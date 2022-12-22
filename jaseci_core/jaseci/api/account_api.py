"""
Account API
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from jaseci.api.interface import Interface
from jaseci.svc.meta import MetaService


class AccountApi:
    """
    Temp
    """

    @Interface.account_api()
    def authorize(self, redirect_url: str):
        """
        Temp
        """

        import os

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        os.environ[
            "OAUTHLIB_RELAX_TOKEN_SCOPE"
        ] = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"

        client_id = (
            "384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com"
        )
        client_secret = "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"

        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "project_id": "oauth-372208",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": ["http://localhost:8001/admin"],
                    "javascript_origins": ["http://localhost:8001"],
                }
            },
            [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid",
            ],
            redirect_uri=redirect_url,
        )

        url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )

        return {"url": url, "state": state}

    @Interface.account_api()
    def exchange(self, state: str, response_url: str, redirect_url: str):
        """
        Temp
        """

        import os

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        os.environ[
            "OAUTHLIB_RELAX_TOKEN_SCOPE"
        ] = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"

        client_id = (
            "384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com"
        )
        client_secret = "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"

        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "project_id": "oauth-372208",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": ["http://localhost:8001/admin"],
                    "javascript_origins": ["http://localhost:8001"],
                }
            },
            [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid",
            ],
            state=state,
            redirect_uri=redirect_url,
        )

        flow.fetch_token(authorization_response=response_url)
        creds: Credentials = flow.credentials
        userinfo = build("oauth2", "v2", credentials=creds)
        print("######################")
        print(userinfo.userinfo().get().execute())
        print("######################")

        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "scopes": creds.scopes,
        }

    @Interface.account_api()
    def refresh(self, credentials: dict):
        """
        Temp
        """

        import os

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        os.environ[
            "OAUTHLIB_RELAX_TOKEN_SCOPE"
        ] = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"

        client_id = (
            "384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com"
        )
        client_secret = "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"

        credentials["token_uri"] = "https://oauth2.googleapis.com/token"
        credentials["client_id"] = client_id
        credentials["client_secret"] = client_secret

        creds = Credentials(**credentials)
        creds.refresh(Request())

        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "scopes": creds.scopes,
        }
