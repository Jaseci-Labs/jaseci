from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import logger, ColCodes as Cc
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
from requests.exceptions import HTTPError
from enum import Enum
from time import time
from json import dumps

from .models import SocialApp

OBJECT_LOG_LIMIT = 5 * 1024 * 1024


class LoginType(Enum):
    REGISTRATION = "New account"
    EXISTING = "Existing account"
    ACTIVATION = "Existing account but just got activated"
    BINDING = "Existing account but just got binded with different login type"


class AppIdFieldNotExists(APIException):
    status_code = 400
    default_detail = "app_id is required!"
    default_code = "Request failed!"


class GetExampleUrlSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SocialLoginProvider.choices)


class JSXSocialLoginSerializer(SocialLoginSerializer):
    app_id = serializers.CharField(required=False, allow_blank=True)

    # deprecated
    internal_client_id = serializers.CharField(required=False, allow_blank=True)

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

        # internal_client_id is deprecated
        app_id = attrs.get("app_id") or attrs.get("internal_client_id")

        if app_id:
            try:
                app = SocialApp.objects.get(id=app_id).legacy()
            except SocialApp.DoesNotExist:
                raise serializers.ValidationError(
                    _(f"app_id is not yet associated on any Social App!"),
                )
        else:
            social_apps = SocialApp.objects.filter(provider=adapter.provider_id)
            social_apps_count = len(social_apps)

            if social_apps_count > 1:
                raise serializers.ValidationError(
                    _(
                        f"You have multiple {adapter.provider_id} Social App. app_id is required to associated it on one of those apps!"
                    ),
                )
            elif social_apps_count < 1:
                raise serializers.ValidationError(
                    _(
                        f"You don't have any Social App for this provider [{adapter.provider_id}]"
                    ),
                )
            else:
                # backward compatibility
                app = social_apps[0].legacy()

        request.app = app
        code = attrs.get("code")

        if code:
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
            attrs = client.get_access_token(code)

        if not attrs.get("access_token") and attrs.get("id_token"):
            attrs["access_token"] = attrs["id_token"]

        social_token = adapter.parse_token(attrs)
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, attrs)
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
        self.request_log()

        self.callback_url = self.get_callback_url(request)
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        data = self.serializer.validated_data
        self.user = data.get("user")

        expiry = (
            knox_settings.TOKEN_TTL
            if knox_settings.TOKEN_TTL
            else timedelta(hours=settings.KNOX_TOKEN_EXPIRY)
        )
        expires_in: str = self.request.query_params.get("expires_in")

        if expires_in and expires_in.isnumeric():
            expiry = None if expires_in == "0" else timedelta(hours=int(expires_in))

        instance, token = AuthToken.objects.create(self.user, expiry)

        auth_user = authenticate(
            request=self.request, username=self.user.email, password=self.user.password
        )
        login_type = data.get("type")
        resp = {
            "email": auth_user.email if auth_user else self.user.email,
            "token": token,
            "exp": instance.expiry,
            "type": login_type.name,
            "details": login_type.value,
        }

        self.response_log(resp)
        return Response(resp)

    def request_log(self):
        request = self.request
        request.start_time = time()
        pl_peek = str(dict(request.data))[:256]
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        extra = {"query": request.GET, "data": request.POST}
        extra["extra_fields"] = list(extra.keys())

        logger.info(
            f"Incoming call to {Cc.TG}{type(self).__name__}{Cc.EC} with {pl_peek} via {user_agent}",
            extra=extra,
        )

    def response_log(self, resp):
        request = self.request
        master = self.user.get_master()
        hook = master._h

        tot_time = time() - request.start_time
        save_count = len(hook.save_obj_list)
        touch_count = len(hook.mem.keys())
        db_touches = hook.db_touch_count
        red_touches = hook.red_touch_count
        touch_kb = hook.mem_size()

        res_peek = str(resp)[:256]
        log_str = str(
            f"API call from {Cc.TG}{master.name}{Cc.EC}:{master.jid}"
            f" to {Cc.TG}{type(self).__name__}{Cc.EC}"
            f" completed in {Cc.TY}{tot_time:.3f} seconds{Cc.EC}"
            f" touched {Cc.TY}{touch_count}{Cc.EC} mem /"
            f" {Cc.TY}{red_touches}{Cc.EC} redis /"
            f" {Cc.TY}{db_touches}{Cc.EC} db "
            f" ({Cc.TY}{touch_kb:.1f}kb{Cc.EC}) and"
            f" saving {Cc.TY}{save_count}{Cc.EC} objects."
            f" Response: {res_peek}."
        )

        log_dict = {
            "api_name": type(self).__name__,
            "request_latency": tot_time,
            "objects_touched": touch_count,
            "redis_touches": red_touches,
            "db_touches": db_touches,
            "objects_touched_size": touch_kb,
            "objects_saved": save_count,
            "caller_name": master.name,
            "caller_jid": master.jid,
        }
        try:
            api_result_str = dumps(resp)[:OBJECT_LOG_LIMIT]
        except TypeError:
            api_result_str = str(resp)[:OBJECT_LOG_LIMIT]
        log_dict["api_response"] = api_result_str
        log_dict["extra_fields"] = list(log_dict.keys())

        logger.info(log_str, extra=log_dict)
