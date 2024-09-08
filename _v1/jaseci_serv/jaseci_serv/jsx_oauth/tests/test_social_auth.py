import jwt
from time import time
from datetime import datetime
from rest_framework.test import APIClient
from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from knox.models import AuthToken
from knox.settings import CONSTANTS
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from jaseci_serv.base.models import User
from jaseci_serv.jsx_oauth.models import SocialApp

mocked_access_token = "ya29.a0AX9GBdVvL b7JjkGJmFOy_oBhQC4jUdOKOjvpHGrcyFjCvWeqwW_1yTkWHJxA6jqEfXYkSzvwBCbq6XsA0o-fTDybsR9T8v8ilXM43IvqIQavWqxebTdjQo5ikPXDabrpJWQ3Uf1gMv1SfnwfeH6KdXxkGwPicaCgYKARwSARMSFQHUCsbCQepIVdu7SMuLZ5c-iI8Awg0163"
mocked_refresh_token = "1//0evz2w3jKj1qUCgYIARAAGA4SNwF-L9IrCiih-u1fKn9ECfKNMtKTK-y6wNZWcTfN8FO1oLnws4QqHkZZn2GSC-GUirdnOORUDIc"
mocked_code = (
    "4%2F0AWgavdcDFN1oZoRrqBlirNICcBprusdJpC0LPYnARjbWOgHGsxJAiw0hVD9zQL3y-rPwnA"
)
mocked_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyYTYxZWZkMmE0NGZjMjE1MTQ4ZDRlZmZjMzRkNmE3YjJhYzI2ZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMzg0NzUyNjExMTkwLWUwNGpiNDNpOGNuZnA5NTNyMW0xZjVtcTVhYmQ5MTlpLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMzg0NzUyNjExMTkwLWUwNGpiNDNpOGNuZnA5NTNyMW0xZjVtcTVhYmQ5MTlpLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTE2NjIwMzI4OTM4NjYyMjkwNDI3IiwiZW1haWwiOiJqYXNlY2kuZGV2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWUd5d2tPZG1VVEo5dU1ma3ZxRGNPZyIsImlhdCI6MTY3MTcwMTQ0MiwiZXhwIjoxNjcxNzA1MDQyfQ.jR23tvfhJYjxHVzOZsdNphZ_2vJ4iPIraY_cbwM9NerfmdiBEhGxhhmksF8X2K5G4Yg607StTjhKNE0XStiWhhBzZu3w7ArujqPoL2NgT2AR8kyQ91cGZcl6REKwhZBQHc7oX9V-UmK6wo8bWfPgdZ0xq_D_YDFaJuabph9d7YutGy4dsEjMkgWN-E1IdVXlXPBciaBK6Djx06x4Wr_dlfeZl0KWHcxWTDXS1DV3rEFpyZlqSTYsTVdnP-nRJZqXbgN7IRNgJIehxBleNRoXCvmm5rD5D1NCI84OOplUEYlpH_dNF8iSdrh7GLgijKl6kbKGlbWyrrBYeJa07nnvJw"


def mocked_get_access_token(*ignored):
    return {
        "access_token": mocked_access_token,
        "expires_in": 3599,
        "refresh_token": mocked_refresh_token,
        "scope": "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "token_type": "Bearer",
        "id_token": mocked_id_token,
    }


def mocked_decode(*ignored_args, **ignored_kwargs):
    t = int(time())
    return {
        "iss": "https://accounts.google.com",
        "azp": "384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com",
        "aud": "384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com",
        "sub": "116620328938662290427",
        "email": "jaseci.dev@gmail.com",
        "email_verified": True,
        "at_hash": "jCcj5Kh-b6LcfHEIVKFJDg",
        "name": "jaseci dev",
        "picture": "https://lh3.googleusercontent.com/a/AEdFTp5FRawOuoF9Tl5jYkExTn1kGbDXqNoJP9ejF6No=s96-c",
        "given_name": "jaseci",
        "family_name": "dev",
        "locale": "en-US",
        "iat": t,
        "exp": t + 1000000,
    }


class SocialAuthTest(TestCaseHelper, TestCase):
    """Test the Social Authentication"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        OAuth2Client.get_access_token = mocked_get_access_token
        jwt.decode = mocked_decode
        self.google_app = SocialApp.objects.create(
            provider="google",
            name="Google OAuth",
            client_id="384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com",
            secret="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",
        )
        self.google_app.save()

    def tearDown(self):
        super().tearDown()

    def create_google_provider(self):
        google_app = SocialApp.objects.create(
            provider="google",
            name="Google OAuth 2",
            client_id="384752611190-e04jb43i8cnfp953r1m1f5mq5abd919i.apps.googleusercontent.com",
            secret="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",
        )

        google_app.save()

        return google_app

    def request_social_sign_in_with_expires_in(self, expires_in_query=""):
        now = datetime.now()

        token = self.client.post(
            path=f"/auth/google/?{expires_in_query}",
            data={"code": mocked_code},
        ).data["token"]

        auth_token = AuthToken.objects.get(
            token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH]
        )

        # convert to hour count if available
        return (
            int((auth_token.expiry - now).total_seconds() / 60 / 60)
            if auth_token.expiry
            else None
        )

    def request_social_sign_in_with_multiple_provider(self, data):
        res = self.client.post(
            path="/auth/google/",
            data=data,
        ).json()

        self.assertEqual(
            {
                "non_field_errors": [
                    "You have multiple google Social App. app_id is required to associated it on one of those apps!"
                ]
            },
            res,
        )
        self.assertEqual(0, User.objects.count())

    def request_social_sign_in(self, data):
        # no user yet
        self.assertEqual(0, User.objects.count())

        res = self.client.post(
            path="/auth/google/",
            data=data,
        ).data

        # user should be created
        self.assertEqual(1, User.objects.count())
        created_user = User.objects.first()

        self.client.credentials(HTTP_AUTHORIZATION="token " + res["token"])

        # token should work
        res = self.client.get(path="/user/manage/").data

        self.assertEqual(
            res,
            {
                "id": 1,
                "email": "jaseci.dev@gmail.com",
                "name": "jaseci dev",
                "is_activated": True,
                "is_superuser": False,
            },
        )

        self.assertEqual(created_user.id, res["id"])
        self.assertEqual(created_user.email, res["email"])
        self.assertEqual(created_user.name, res["name"])
        self.assertEqual(created_user.is_activated, res["is_activated"])
        self.assertIsNotNone(created_user.get_master())

        # getting token again should not create another user
        res = self.client.post(
            path="/auth/google/",
            data=data,
        ).data

        # user count should still be the same
        self.assertEqual(1, User.objects.count())
        self.assertEqual(created_user, User.objects.first())

        User.objects.all().delete()

    def test_social_auth_flow_using_authorization_code(self):
        """Test social auth flow from 'with autorization code'"""
        self.request_social_sign_in({"code": mocked_code})

    def test_social_auth_flow_using_id_token(self):
        """Test social auth flow from 'with id token'"""
        self.request_social_sign_in({"id_token": mocked_id_token})

    def test_social_auth_flow_using_access_token(self):
        """Test social auth flow from 'with access token'"""
        self.request_social_sign_in(mocked_get_access_token())

    def test_social_auth_flow_with_multiple_provider(self):
        """Test social auth flow from 'with autorization code'"""

        self.create_google_provider()

        self.request_social_sign_in_with_multiple_provider(
            {
                "code": mocked_code,
            }
        )

        self.request_social_sign_in_with_multiple_provider(
            {"id_token": mocked_id_token}
        )

        self.request_social_sign_in_with_multiple_provider(mocked_get_access_token())

    def test_social_auth_flow_using_authorization_code_with_app_id(self):
        self.request_social_sign_in(
            {"app_id": self.create_google_provider().id, "code": mocked_code}
        )

    def test_social_auth_flow_using_id_token_with_app_id(self):
        self.request_social_sign_in(
            {
                "app_id": self.create_google_provider().id,
                "id_token": mocked_id_token,
            }
        )

    def test_social_auth_flow_using_access_token_with_app_id(self):
        data = mocked_get_access_token()
        data["app_id"] = self.create_google_provider().id
        self.request_social_sign_in(data)

    def test_social_auth_flow_with_expires_in_param(self):
        # no expires_in_param: defaults to 12 hrs
        self.assertEqual(12, self.request_social_sign_in_with_expires_in())

        # expires_in: 24 hrs
        self.assertEqual(
            24, self.request_social_sign_in_with_expires_in("expires_in=24")
        )

        # no expiry
        self.assertEqual(
            None, self.request_social_sign_in_with_expires_in("expires_in=0")
        )
