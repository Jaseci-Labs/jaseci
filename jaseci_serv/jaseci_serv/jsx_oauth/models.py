from pyexpat import model
from jaseci_serv.base.models import *
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        "LOGIN_URL": "https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={callback_url}&prompt=consent&response_type=code&client_id={client_id}&scope=openid%20email%20profile&access_type=offline",
        "DEFAULT_REDIRECT_URI": "/auth/examples/google/",
    },
    SocialLoginProvider.FACEBOOK: {
        "URL_KEY": SocialLoginProvider.FACEBOOK + "_REDIRECT_URI",
        "LOGIN_URL": "https://www.facebook.com/v15.0/dialog/oauth?client_id={client_id}&redirect_uri={callback_url}&state={{st=state123abc,ds=123456789}}",
        "DEFAULT_REDIRECT_URI": "/auth/examples/facebook/",
    },
    SocialLoginProvider.GITHUB: {
        "URL_KEY": SocialLoginProvider.GITHUB + "_REDIRECT_URI",
        "LOGIN_URL": "",
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


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
