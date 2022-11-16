import os
from .base import *

ADDITIONAL_APPS = [
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.microsoft",
    "allauth.socialaccount.providers.okta",
    # "allauth.socialaccount.providers.openid",
    "jaseci_serv.jsx_oauth",
]

INSTALLED_APPS += ADDITIONAL_APPS


AUTH_PROVIDERS = {"facebook": "facebook", "google": "google", "email": "email"}

SOCIAL_AUTH_CREDS = {
    "google": {
        "GOOGLE_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET"),
    },
    "facebook": {
        "FACEBOOK_CLIENT_ID": os.environ.get("FACEBOOK_CLIENT_ID"),
        "FACEBOOK_CLIENT_SECRET": os.environ.get("FACEBOOK_CLIENT_SECRET"),
    },
}

JSX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES[0]["DIRS"] += [os.path.join(JSX_DIR, "templates")]
KNOX_TOKEN_EXPIRY = 24

REST_AUTH_TOKEN_MODEL = None

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

SITE_ID = 1
