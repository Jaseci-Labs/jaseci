from django.test import TestCase
from django.urls import NoReverseMatch
from jaseci.utils.utils import TestCaseHelper
from rest_framework.test import APIClient

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
        self.master = self.user.get_master()
        self.client.force_authenticate(self.admin_user)

    def test_stripe_init_should_return_forbidden_response(self):
        """should reutnr forbidden response"""
        res = self.client.post(reverse("stripe_init"))

        self.assertEqual(res.status_code, 403)
        self.assertFalse(res.json()["success"])
        self.assertTrue(
            res.json()["message"]
            == "Stripe is not yet configured. Please set a valid stripe key."
        )

    def test_stripe_init_returns_stripe_webhook_url(self):
        """/stripe/init"""
        GlobalVars.objects.create(
            name="STRIPE_API_KEY",
            value="sk_test_4eC39HqLyjWDarjtT1zdp7dc",
        )

        res = self.client.post(reverse("stripe_init"))

        print(res)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])
        self.assertTrue(res.json()["data"].startswith("/js_public/walker_callback/"))
