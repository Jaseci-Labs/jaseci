from uuid import uuid4
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from jaseci_enterprise.jsx_oauth.models import LicenseCheckStatus
from allauth.socialaccount.models import SocialApp
from datetime import datetime, timedelta


GOOGLE_CLIENT_ID = (
    "582296225245-3kqi04d89ahlk1kr8j15j1uolci0hrtq.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"
GET_TEST_URL = reverse("get_test_url")
SSO_PROVIDER = "GOOGLE"
TOKEN_URL = reverse("user_api:token")
MANAGE_URL = reverse("user_api:manage")
LOGOUT_EVERYONE_URL = reverse("user_api:logout_everyone")
PASSWORD_RESET_URL = reverse("user_api:password_reset:reset-password-request")
# Alias for create user
create_user = get_user_model().objects.create_user
create_superuser = get_user_model().objects.create_superuser
get_user = get_user_model().objects.get


def toggle_license_validation(make_valid=True):
    if make_valid:
        lcs = LicenseCheckStatus.objects.create(
            last_checked=datetime.now() - timedelta(days=3),
            license_validity=datetime.now() + timedelta(days=30),
            license_status=True,
            is_user_active=True,
        )
        return lcs
    else:
        lcs = LicenseCheckStatus.objects.create(
            last_checked=datetime.now() - timedelta(days=30),
            license_validity=datetime.now() - timedelta(days=3),
            license_status=False,
            is_user_active=False,
        )

        return lcs


class JSXUserApiPublicTests(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.user = create_user(
            email="jscitest_test@jaseci.com",
            password="testpass",
            name="some dude",
        )
        self.social_app = SocialApp.objects.create(
            provider="google",
            name="google",
            client_id=GOOGLE_CLIENT_ID,
            secret=GOOGLE_CLIENT_SECRET,
        )
        self.client = APIClient()
        # self.toggle_license_validation
        # self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()
        super().tearDown()

    def test_response_on_expired_license(self):
        """Test API response When license Expired"""
        toggle_license_validation(False)
        payload = {"provider": "GOOGLE"}
        res = self.client.post(GET_TEST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_response_on_valid_license(self):
        """Test API response When license Expired"""
        toggle_license_validation(True)
        payload = {"provider": "GOOGLE"}
        res = self.client.post(GET_TEST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
