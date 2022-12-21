from jaseci_serv.jsx_oauth.models import PROVIDERS_MAPPING
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from jaseci_serv.base.models import lookup_global_config
from django.conf import settings
from knox.settings import knox_settings
from knox.models import AuthToken
from django.contrib.auth import authenticate, get_user_model
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import serializers
from allauth.socialaccount.helpers import complete_social_login
from allauth.account import app_settings as allauth_settings
from requests.exceptions import HTTPError


class JSXSocialLoginSerializer(SocialLoginSerializer):
    def validate(self, attrs):
        view = self.context.get("view")
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable"),
            )

        adapter_class = getattr(view, "adapter_class", None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        access_token = attrs.get("access_token")
        code = attrs.get("code")
        # Case 1: We received the access_token
        if access_token:
            tokens_to_parse = {"access_token": access_token}
            token = access_token
            # For sign in with apple
            id_token = attrs.get("id_token")
            if id_token:
                tokens_to_parse["id_token"] = id_token

        # Case 2: We received the authorization code
        elif code:
            self.set_callback_url(view=view, adapter_class=adapter_class)
            self.client_class = getattr(view, "client_class", None)

            if not self.client_class:
                raise serializers.ValidationError(
                    _("Define client_class in view"),
                )
            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth,
            )
            token = client.get_access_token(code)
            access_token = token["access_token"]
            tokens_to_parse = {"access_token": access_token}

            # If available we add additional data to the dictionary
            for key in ["refresh_token", "id_token", adapter.expires_in_key]:
                if key in token:
                    tokens_to_parse[key] = token[key]
        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token or code is required."),
            )

        social_token = adapter.parse_token(tokens_to_parse)
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError("Incorrect value")

        if not login.is_existing:
            if allauth_settings.UNIQUE_EMAIL:
                # Do we have an account already with this email address?
                account_exists = (
                    get_user_model()
                    .objects.filter(
                        email=login.user.email,
                    )
                    .exists()
                )
                if account_exists:
                    raise serializers.ValidationError(
                        _("User is already registered with this e-mail address."),
                    )

            login.lookup()
            login.save(request, connect=True)
        attrs["user"] = login.account.user
        if "name" in login.account.extra_data.keys():
            attrs["name"] = login.account.extra_data.get("name", "")
        return attrs


class JSXSocialLoginView(SocialLoginView):
    adapter_class = None
    provider = None
    client_class = OAuth2Client
    serializer_class = JSXSocialLoginSerializer
    # permission_classes = [IsValidateLicense, AllowAny]

    def get_callback_url(self):
        if self.provider:
            REDIRECT_URI = resolve(PROVIDERS_MAPPING[self.provider]["URL_KEY"])
            if REDIRECT_URI:
                return REDIRECT_URI
            if self.request:
                return f"{self.request.build_absolute_uri('/')[:-1]}{settings.DEFAULT_CALLBACK_URL_FOR_SSO}"
            return None

        raise RuntimeError(
            "Provider name cannot be empty or None. "
            'Please provide a valid provider name e.g. "GOOGLE"'
        )

    def dispatch(self, *args, **kwargs):
        self.callback_url = self.get_callback_url()
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.user = self.serializer.validated_data.get("user")
        # self.login()
        self.user.is_activated = True
        self.user.name = self.serializer.validated_data.get("name")
        self.user.save()
        auth_token = AuthToken.objects.filter(user_id=self.user.id)
        if auth_token:
            AuthToken.objects.filter(user_id=self.user.id).delete()
        instance, token = AuthToken.objects.create(
            self.user,
            knox_settings.TOKEN_TTL
            if knox_settings.TOKEN_TTL
            else timedelta(hours=settings.KNOX_TOKEN_EXPIRY),
        )

        auth_user = authenticate(
            request=self.request, username=self.user.email, password=self.user.password
        )
        return Response(
            {
                "email": auth_user.email if auth_user else self.user.email,
                "token": token,
                "exp": instance.expiry,
            }
        )


def resolve(name):
    try:
        return lookup_global_config(
            name=name, default=social_auth_config_defaults[name]
        )
    except Exception as e:
        return None
