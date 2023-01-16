import jwt
from time import time
from rest_framework.test import APIClient
from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from jaseci_serv.base.models import User


def mocked_get_access_token(*ignored):
    return {
        "access_token": "ya29.a0AX9GBdVvL b7JjkGJmFOy_oBhQC4jUdOKOjvpHGrcyFjCvWeqwW_1yTkWHJxA6jqEfXYkSzvwBCbq6XsA0o-fTDybsR9T8v8ilXM43IvqIQavWqxebTdjQo5ikPXDabrpJWQ3Uf1gMv1SfnwfeH6KdXxkGwPicaCgYKARwSARMSFQHUCsbCQepIVdu7SMuLZ5c-iI8Awg0163",
        "expires_in": 3599,
        "refresh_token": "1//0evz2w3jKj1qUCgYIARAAGA4SNwF-L9IrCiih-u1fKn9ECfKNMtKTK-y6wNZWcTfN8FO1oLnws4QqHkZZn2GSC-GUirdnOORUDIc",
        "scope": "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "token_type": "Bearer",
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyYTYxZWZkMmE0NGZjMjE1MTQ4ZDRlZmZjMzRkNmE3YjJhYzI2ZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMzg0NzUyNjExMTkwLWUwNGpiNDNpOGNuZnA5NTNyMW0xZjVtcTVhYmQ5MTlpLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMzg0NzUyNjExMTkwLWUwNGpiNDNpOGNuZnA5NTNyMW0xZjVtcTVhYmQ5MTlpLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTE2NjIwMzI4OTM4NjYyMjkwNDI3IiwiZW1haWwiOiJqYXNlY2kuZGV2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWUd5d2tPZG1VVEo5dU1ma3ZxRGNPZyIsImlhdCI6MTY3MTcwMTQ0MiwiZXhwIjoxNjcxNzA1MDQyfQ.jR23tvfhJYjxHVzOZsdNphZ_2vJ4iPIraY_cbwM9NerfmdiBEhGxhhmksF8X2K5G4Yg607StTjhKNE0XStiWhhBzZu3w7ArujqPoL2NgT2AR8kyQ91cGZcl6REKwhZBQHc7oX9V-UmK6wo8bWfPgdZ0xq_D_YDFaJuabph9d7YutGy4dsEjMkgWN-E1IdVXlXPBciaBK6Djx06x4Wr_dlfeZl0KWHcxWTDXS1DV3rEFpyZlqSTYsTVdnP-nRJZqXbgN7IRNgJIehxBleNRoXCvmm5rD5D1NCI84OOplUEYlpH_dNF8iSdrh7GLgijKl6kbKGlbWyrrBYeJa07nnvJw",
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
        self.google_app.sites.add(
            Site.objects.first(),
            Site.objects.create(domain="google.com", name="google"),
        )
        self.google_app.save()

    def tearDown(self):
        super().tearDown()

    def test_social_auth_flow(self):
        """Test social auth flow from 'with autorization code'"""

        # no user yet
        self.assertEqual(0, User.objects.count())

        res = self.client.post(
            path="/auth/google/",
            data={
                "id_token": "",
                "code": "4%2F0AWgavdcDFN1oZoRrqBlirNICcBprusdJpC0LPYnARjbWOgHGsxJAiw0hVD9zQL3y-rPwnA",
                "access_token": "",
            },
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

        # getting token again should create another user
        res = self.client.post(
            path="/auth/google/",
            data={
                "id_token": "",
                "code": "4%2F0AWgavdcDFN1oZoRrqBlirNICcBprusdJpC0LPYnARjbWOgHGsxJAiw0hVD9zQL3y-rPwnA",
                "access_token": "",
            },
        ).data

        # user count should still be the same
        self.assertEqual(1, User.objects.count())
        self.assertEqual(created_user, User.objects.first())
