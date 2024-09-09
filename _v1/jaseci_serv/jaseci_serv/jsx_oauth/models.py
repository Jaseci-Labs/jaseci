from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.models import SocialApp as LegacySocialApp
from allauth.socialaccount import providers


class SocialLoginProvider(models.TextChoices):
    GOOGLE = "GOOGLE", _("Google")
    FACEBOOK = "FACEBOOK", _("Facebook")
    MICROSOFT = "MICROSOFT", _("Microsoft")
    GITHUB = "GITHUB", _("GitHub")
    OKTA = "OKTA", _("Okta")
    OPENID = "OPENID", _("OpenID")
    APPLE = "APPLE", _("Apple")


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
    SocialLoginProvider.APPLE: {
        "URL_KEY": SocialLoginProvider.APPLE + "_REDIRECT_URI",
        "LOGIN_URL": "",
        "DEFAULT_REDIRECT_URI": "/auth/examples/apple/",
    },
}


class SocialApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name=_("name"), max_length=40)
    provider = models.CharField(
        verbose_name=_("provider"),
        max_length=30,
        choices=providers.registry.as_choices(),
    )
    client_id = models.CharField(
        verbose_name=_("client id"),
        max_length=191,
        help_text=_("App ID, or consumer key"),
    )
    secret = models.CharField(
        verbose_name=_("secret key"),
        max_length=191,
        blank=True,
        help_text=_("API secret, client secret, or consumer secret"),
    )
    key = models.CharField(
        verbose_name=_("key"), max_length=191, blank=True, help_text=_("Key")
    )

    certificate_key = models.TextField(verbose_name=_("certificate key"), blank=True)

    class Meta:
        verbose_name = _("social application")
        verbose_name_plural = _("social applications")

    def __str__(self):
        return self.name

    def legacy(self):
        app = LegacySocialApp(
            provider=self.provider,
            name=self.name,
            client_id=self.client_id,
            secret=self.secret,
            key=self.key,
        )
        app.certificate_key = self.certificate_key
        return app
