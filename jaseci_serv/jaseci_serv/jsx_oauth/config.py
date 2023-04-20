import os

OAUTH_APPS = [
    "rest_framework.authtoken",
    "dj_rest_auth",
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
]


AUTH_PROVIDERS = {"facebook": "facebook", "google": "google", "email": "email"}
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

KNOX_TOKEN_EXPIRY = 12

REST_AUTH_TOKEN_MODEL = None

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
