import random
import string
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from allauth.socialaccount.providers.okta.views import OktaOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.views import (
    AppleOAuth2Adapter as LegacyAppleOAuth2Adapter,
    AppleOAuth2Client,
)
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter, get_adapter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from jaseci_serv.jsx_oauth.utils import GetExampleUrlSerializer
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from jaseci_serv.jsx_oauth.models import (
    SocialLoginProvider,
    PROVIDERS_MAPPING,
    SocialApp,
)
from jaseci_serv.jsx_oauth.utils import JSXSocialLoginView

#################################################
#     OVERRIDING DEFAULTS FOR APPLE SIGN IN     #
#################################################

main_get_app = DefaultSocialAccountAdapter.get_app


def custom_get_app(self, request, provider, config=None):
    if hasattr(request, "app") and request.app:
        return request.app
    return main_get_app(self, request, provider, config)


DefaultSocialAccountAdapter.get_app = custom_get_app


class AppleOAuth2Adapter(LegacyAppleOAuth2Adapter):
    def get_client_id(self, provider):
        app = get_adapter().get_app(self.request, provider)
        return [aud.strip() for aud in app.client_id.split(",")]


# --------------------------------------------- #


def generate_state():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=64
        )
    )


class ExampleUrlView(GenericAPIView):
    serializer_class = GetExampleUrlSerializer

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        provider = serializer_data.validated_data.get("provider")
        provider_map = PROVIDERS_MAPPING[provider]
        callback_url = f'{request.build_absolute_uri("/")[:-1]}{provider_map["DEFAULT_REDIRECT_URI"]}'
        social_app = SocialApp.objects.filter(provider=provider.lower()).first()
        if social_app:
            return Response(
                {
                    "url": provider_map["LOGIN_URL"].format(
                        callback_url=callback_url,
                        client_id=social_app.client_id,
                        state=generate_state(),
                    )
                }
            )
        else:
            return Response(
                {
                    "error": f"Social login applications for the {provider} not configured properly"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GoogleLogin(JSXSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    provider = SocialLoginProvider.GOOGLE
    client_class = OAuth2Client


class FaceBookLogin(JSXSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    provider = SocialLoginProvider.FACEBOOK
    client_class = OAuth2Client


class GitHubLogin(JSXSocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    provider = SocialLoginProvider.GITHUB
    client_class = OAuth2Client


class OktaLogin(JSXSocialLoginView):
    adapter_class = OktaOAuth2Adapter
    provider = SocialLoginProvider.OKTA
    client_class = OAuth2Client


class MicrosoftLogin(JSXSocialLoginView):
    adapter_class = MicrosoftGraphOAuth2Adapter
    provider = SocialLoginProvider.MICROSOFT
    client_class = OAuth2Client


class OpenIdLogin(JSXSocialLoginView):
    adapter_class = GitHubOAuth2Adapter  # TODO: create custom adaptor for OpenID
    provider = SocialLoginProvider.OPENID
    client_class = OAuth2Client


class AppleLogin(JSXSocialLoginView):
    adapter_class = AppleOAuth2Adapter
    provider = SocialLoginProvider.APPLE
    client_class = AppleOAuth2Client


@method_decorator(csrf_exempt, name="dispatch")
class ExampleLiveView(View):
    template_name = "examples/social_auth.html"

    def get(self, request, provider):
        code = request.GET.get("code")
        social_app = SocialApp.objects.filter(provider=provider).first()
        return render(
            request,
            self.template_name,
            {
                "provider": provider,
                "code": code,
                "client_id": social_app.client_id,
                "state": generate_state(),
            },
        )

    def post(self, request, provider):
        data = request.POST.dict()
        return render(
            request,
            self.template_name,
            {
                "provider": provider,
                "id_token": data["id_token"],
                "state": data["state"],
            },
        )
