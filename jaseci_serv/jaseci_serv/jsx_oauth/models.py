from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.models import SocialApp


class SocialLoginProvider(models.TextChoices):
    GOOGLE = "GOOGLE", _("Google")
    FACEBOOK = "FACEBOOK", _("Facebook")
    MICROSOFT = "MICROSOFT", _("Microsoft")
    GITHUB = "GITHUB", _("GitHub")
    OKTA = "OKTA", _("Okta")
    OPENID = "OPENID", _("OpenID")


PROVIDERS_MAPPING = {
    SocialLoginProvider.GOOGLE: {
        "URL_KEY": SocialLoginProvider.GOOGLE + "_REDIRECT_URI",
        "LOGIN_URL": "https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={callback_url}&prompt=consent&response_type=code&client_id={client_id}&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid",
        "DEFAULT_REDIRECT_URI": "/auth/examples/google/",
    },
    SocialLoginProvider.FACEBOOK: {
        "URL_KEY": SocialLoginProvider.FACEBOOK + "_REDIRECT_URI",
        "LOGIN_URL": "https://www.facebook.com/dialog/oauth/?client_id={client_id}&redirect_uri={callback_url}&scope=email&state={state}",
        "DEFAULT_REDIRECT_URI": "/auth/examples/facebook/",
    },
    SocialLoginProvider.GITHUB: {
        "URL_KEY": SocialLoginProvider.GITHUB + "_REDIRECT_URI",
        "LOGIN_URL": "https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={callback_url}&scope=read:user,user:email&state={state}",
        "DEFAULT_REDIRECT_URI": "/auth/examples/github/",
    },
    SocialLoginProvider.MICROSOFT: {
        "URL_KEY": SocialLoginProvider.MICROSOFT + "_REDIRECT_URI",
        "LOGIN_URL": "",
        "DEFAULT_REDIRECT_URI": "/auth/examples/microsoft/",
    },
    SocialLoginProvider.OKTA: {
        "URL_KEY": SocialLoginProvider.OKTA + "_REDIRECT_URI",
        "LOGIN_URL": "",
        "DEFAULT_REDIRECT_URI": "/auth/examples/okta/",
    },
    SocialLoginProvider.OPENID: {
        "URL_KEY": SocialLoginProvider.OPENID + "_REDIRECT_URI",
        "LOGIN_URL": "",
        "DEFAULT_REDIRECT_URI": "/auth/examples/openid/",
    },
}


class InternalClient(models.Model):
    """
    Add internal_client_id on social app model
    """

    name = models.CharField(max_length=255)
    client_id = models.UUIDField(default=uuid4, unique=True)
    social_app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
