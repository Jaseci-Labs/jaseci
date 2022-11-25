from django.test import TestCase
from django.urls import NoReverseMatch
from jaseci.utils.utils import TestCaseHelper
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from jaseci_serv.base.models import GlobalVars
from django.urls import reverse


class ApiTest(TestCaseHelper, TestCase):
    def setUp(self):
        """Creates test client, admin user and user for this test case"""
        super().setUp()
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="JSCITEST_admin@jaseci.com", password="password"
        )
        self.user = get_user_model().objects.create_user(
            email="JSCITEST_test@jaseci.com", password="password"
        )
        self.client.force_authenticate(self.admin_user)
        self.master = self.user.get_master()

    def tearDown(self):
        """Deletes test users and sample stripe_api_key out of databases"""
        self.admin_user.delete()
        self.user.delete()
        super().tearDown()

    def test_stripe_init_returns_stripe_webhook_url(self):
        """/stripe/init"""
        # self.master._h.save_glob(
        #     "STRIPE_API_KEY",
        #     "sk_test_4eC39HqLyjWDarjtT1zdp7dc",
        # )
        GlobalVars.objects.create(
            name="STRIPE_API_KEY",
            value="sk_test_4eC39HqLyjWDarjtT1zdp7dc",
        )

        res = self.client.post(reverse("stripe_init"))

        # print(res.json())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["success"])
        self.assertTrue(res.json()["data"].startswith("/js_public/walker_callback/"))

    def test_stripe_init_should_return_forbidden_response(self):
        """should return forbidden response"""

        # self.master._h.destroy_glob(
        #     "STRIPE_API_KEY"
        # )

        GlobalVars.objects.filter(name="STRIPE_API_KEY").delete()

        if self.master._h.get_glob("STRIPE_API_KEY"):
            self.master._h.destroy_glob("STRIPE_API_KEY")

        res = self.client.post(reverse("stripe_init"))

        # print(res.json())

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(res.json()["success"])
        self.assertTrue(
            res.json()["message"]
            == "Stripe is not yet configured. Please set a valid stripe key."
        )
