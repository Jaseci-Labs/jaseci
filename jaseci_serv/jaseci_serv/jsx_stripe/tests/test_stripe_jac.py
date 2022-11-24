import uuid
import base64
import os

from django.test import TestCase
from django.urls import reverse
from ..models import JSX_STRIPE_DIR
from jaseci.utils.utils import TestCaseHelper
from rest_framework.test import APIClient
from rest_framework import status


from django.contrib.auth import get_user_model
from jaseci_serv.base.models import GlobalVars


class testStripeJac(TestCaseHelper, TestCase):
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

        STRIPE_JAC = os.path.join(JSX_STRIPE_DIR, "stripe.jac")
        ll_file = base64.b64encode(open(STRIPE_JAC).read().encode()).decode()
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": ll_file,
            "encoded": True,
        }

        res = self.client.post(reverse("jac_api:sentinel_register"), payload)
        self.snt = self.master._h.get_obj(
            self.master.jid, str(uuid.UUID(res.data[0]["jid"]))
        )
        self.gph = self.master._h.get_obj(
            self.master.jid, str(uuid.UUID(res.data[1]["jid"]))
        )

        GlobalVars.objects.create(
            name="STRIPE_API_KEY",
            value="sk_test_4eC39HqLyjWDarjtT1zdp7dc",
        )

        res = self.client.post(reverse("stripe_init"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["success"])
        self.assertTrue(res.json()["data"].startswith("/js_public/walker_callback/"))

    def test_create_product(self):
        """test create_product walker"""

        payload = {
            "name": "create_product",
            "ctx": {
                "name": "test@gmail.com",
                "description": "test user",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_product_price(self):
        """test create_product_price walker"""

        payload = {
            "name": "create_product_price",
            "ctx": {
                "productId": "testProductId",
                "amount": 12,
                "currency": "usd",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_product_list(self):
        """test product_list walker"""

        payload = {
            "name": "product_list",
            "ctx": {
                "detailed": True,
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_product_price(self):
        """test create_product_price walker"""

        payload = {
            "name": "create_product_price",
            "ctx": {
                "productId": "testProductId",
                "amount": 12,
                "currency": "usd",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_customer(self):
        """test create_customer walker"""

        payload = {
            "name": "create_customer",
            "ctx": {
                "email": "test@gmail.com",
                "name": "test user",
                "metadata": {"user_id": "123", "node_id": "test_node_id"},
                "payment_method_id": "test_payment_method",
                "address": "my address",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_customer(self):
        """test get_customer walker"""

        payload = {
            "name": "get_customer",
            "ctx": {
                "customer_id": "customer_id1",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_attach_payment_method(self):
        """test attach_payment_method walker"""

        payload = {
            "name": "attach_payment_method",
            "ctx": {
                "payment_method_id": "payment_method_id",
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_delete_payment_method(self):
        """test delete_payment_method walker"""

        payload = {
            "name": "delete_payment_method",
            "ctx": {
                "payment_method_id": "payment_method_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_payment_methods(self):
        """test get_payment_methods walker"""

        payload = {
            "name": "get_payment_methods",
            "ctx": {
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_update_default_payment_method(self):
        """test update_default_payment_method walker"""

        payload = {
            "name": "update_default_payment_method",
            "ctx": {
                "payment_method_id": "payment_method_id",
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_invoice(self):
        """test create_invoice walker"""

        payload = {
            "name": "create_invoice",
            "ctx": {
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_invoice_list(self):
        """test get_invoice_list walker"""

        payload = {
            "name": "get_invoice_list",
            "ctx": {
                "customer_id": "customer_id",
                "subscription_id": "subscription_id",
                "starting_after": "starting_after",
                "limit": 12,
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_payment_intents(self):
        """test get_payment_intents walker"""

        payload = {
            "name": "get_payment_intents",
            "ctx": {
                "customer_id": "customer_id",
                "starting_after": "starting_after",
                "limit": 12,
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_payment_intents(self):
        """test create_payment_intents walker"""

        payload = {
            "name": "create_payment_intents",
            "ctx": {
                "amount": 12,
                "currency": "currency",
                "payment_method_types": "payment_method_types",
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_customer_subscription(self):
        """test get_customer_subscription walker"""

        payload = {
            "name": "get_customer_subscription",
            "ctx": {
                "customer_id": "customer_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_payment_method(self):
        """test create_payment_method walker"""

        payload = {
            "name": "create_payment_method",
            "ctx": {
                "card_type": "card_type",
                "card": "card",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_trial_subscription(self):
        """test create_trial_subscription walker"""

        payload = {
            "name": "create_trial_subscription",
            "ctx": {
                "payment_method_id": "card_type",
                "price_id": "card",
                "customer_id": "card",
                "trial_period_days": 30,
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_subscription(self):
        """test create_subscription walker"""

        payload = {
            "name": "create_subscription",
            "ctx": {
                "payment_method_id": "card_type",
                "price_id": "card",
                "customer_id": "card",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_cancel_subscription(self):
        """test cancel_subscription walker"""

        payload = {
            "name": "cancel_subscription",
            "ctx": {
                "subscription_id": "subscription_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_subscription(self):
        """test get_subscription walker"""

        payload = {
            "name": "get_subscription",
            "ctx": {
                "subscription_id": "subscription_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_update_subscription(self):
        """test update_subscription walker"""

        payload = {
            "name": "update_subscription",
            "ctx": {
                "subscription_id": "subscription_id",
                "subscription_item_id": "subscription_item_id",
                "price_id": "price_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_get_invoice(self):
        """test get_invoice walker"""

        payload = {
            "name": "get_invoice",
            "ctx": {
                "invoice_id": "invoice_id",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])

    def test_create_usage_report(self):
        """test create_usage_report walker"""

        payload = {
            "name": "create_usage_report",
            "ctx": {
                "subscription_item_id": "subscription_item_id",
                "quantity": "quantity",
                "mock_api": True,
            },
        }

        res = self.client.post("/js/walker_run", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()["report"][0]["success"])
