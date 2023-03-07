from jaseci import JsOrc
from jaseci_serv.jsx_oauth.models import PROVIDERS_MAPPING, SocialLoginProvider
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from jaseci_serv.base.models import lookup_global_config
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from knox.settings import knox_settings
from knox.models import AuthToken
from django.contrib.auth import authenticate, get_user_model
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import serializers
from allauth.socialaccount.helpers import complete_social_login
from allauth.account import app_settings as allauth_settings
from requests.exceptions import HTTPError
from enum import Enum


class LoginType(Enum):
    REGISTRATION = "New account"
    EXISTING = "Existing account"
    ACTIVATION = "Existing account but just got activated"
    BINDING = "Existing account but just got binded with different login type"


class RegistrationConflict(APIException):
    status_code = 409
    default_detail = "User is already registered with this e-mail address!"
    default_code = "Registration failed!"


class GetExampleUrlSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SocialLoginProvider.choices)


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
            raise serializers.ValidationError(_("Incorrect value"))

        attrs["type"] = LoginType.EXISTING

        if not login.is_existing:
            login.lookup()
            try:
                user = get_user_model().objects.get(
                    email=login.user.email,
                )
                login.user = user
                attrs["type"] = LoginType.BINDING
            except ObjectDoesNotExist:
                pass
            login.save(request, connect=True)

        user = login.account.user
        attrs["user"] = user

        if not user.is_activated:
            user.is_activated = True
            if user.has_usable_password():
                attrs["type"] = LoginType.ACTIVATION
            else:
                if "name" in login.account.extra_data.keys():
                    user.name = login.account.extra_data.get("name", "")
                user.master = JsOrc.master(h=user._h, name=user.email).id
                attrs["type"] = LoginType.REGISTRATION

            user._h.commit()
            user.save()

        return attrs


class JSXSocialLoginView(SocialLoginView):
    adapter_class = None
    provider = None
    client_class = OAuth2Client
    serializer_class = JSXSocialLoginSerializer
    # permission_classes = [IsValidateLicense, AllowAny]

    def get_callback_url(self, request):
        callback_url = request.data.get("callback_url")
        if callback_url:
            return callback_url

        if self.provider:
            prov = PROVIDERS_MAPPING[self.provider]
            return lookup_global_config(
                name=prov["URL_KEY"],
                default=f'{request.build_absolute_uri("/")[:-1]}{prov["DEFAULT_REDIRECT_URI"]}',
            )
        raise RuntimeError(
            "Provider name cannot be empty or None. "
            'Please provide a valid provider name e.g. "GOOGLE"'
        )

    def post(self, request, *args, **kwargs):
        self.request = request
        self.callback_url = self.get_callback_url(request)
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        data = self.serializer.validated_data
        self.user = data.get("user")
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
        login_type = data.get("type")
        return Response(
            {
                "email": auth_user.email if auth_user else self.user.email,
                "token": token,
                "exp": instance.expiry,
                "type": login_type.name,
                "details": login_type.value,
            }
        )
