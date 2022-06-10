"""
This module includes code related to configuring Jaseci's Social Auth serving
"""
from jaseci_serv.base.models import lookup_global_config
from jaseci_serv.jaseci_serv.settings import EMAIL_BACKEND
from django.core import mail
from jaseci.utils.utils import logger


social_auth_config_defaults = {
    "GOOGLE_CLIENT_ID": "582296225245-3kqi04d89ahlk1kr8j15j1uolci0hrtq.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "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",
    "FACEBOOK_CLIENT_ID": "",
    "FACEBOOK_CLIENT_SECRET": "",
    "GLOBAL_SOCIAL_SECRET": "9Pe7o42EpeDBC7cOs1KybETm611L0kHa",
}


class socialauth_config:
    # def __init__(self):
    # self.setup_socialauth_creds()
    # self.setup_email_templates()

    def get_auth_conf(self, auth_type=""):
        """Loads an email connection relative to global configs"""

        def resolve(name):
            return lookup_global_config(
                name=name, default=social_auth_config_defaults[name]
            )

        GOOGLE_CLIENT_ID = resolve("GOOGLE_CLIENT_ID")
        GOOGLE_CLIENT_SECRET = resolve("GOOGLE_CLIENT_SECRET")
        FACEBOOK_CLIENT_ID = resolve("FACEBOOK_CLIENT_ID")
        FACEBOOK_CLIENT_SECRET = resolve("FACEBOOK_CLIENT_SECRET")
        socialauth_cred = {
            "google": {
                "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
                "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
            },
            "facebook": {
                "FACEBOOK_CLIENT_ID": FACEBOOK_CLIENT_ID,
                "FACEBOOK_CLIENT_SECRET": FACEBOOK_CLIENT_SECRET,
            },
        }
        if auth_type:
            return socialauth_cred[auth_type.lower()]
        else:
            return socialauth_cred

    def get_social_secret(self):
        """Loads an email connection relative to global configs"""

        def resolve(name):
            return lookup_global_config(
                name=name, default=social_auth_config_defaults[name]
            )

        return resolve("GLOBAL_SOCIAL_SECRET")
