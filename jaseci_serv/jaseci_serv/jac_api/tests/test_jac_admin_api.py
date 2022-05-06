from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase


class PrivateJacAdminApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        # First user is always super,
        self.user = get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.nonadmin = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.notadminc = APIClient()
        self.notadminc.force_authenticate(self.nonadmin)
        self.master = self.user.get_master()

    def tearDown(self):
        super().tearDown()

    def test_jac_api_config_index_has_core(self):
        payload = {"op": "config_index"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data), 2)
        self.assertIn("ACTION_SETS", res.data)

    def test_jac_api_create_config(self):
        """Test API for creating a config"""
        payload = {
            "op": "config_set",
            "name": "EMAIL_HOST_USER",
            "value": "val1",
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {"op": "config_get", "name": "EMAIL_HOST_USER"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "val1")

    def test_jac_api_create_config_needs_force(self):
        """Test API for creating a config"""
        payload = {"op": "config_delete", "name": "TEST"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "config_set", "name": "TEST", "value": "val1"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {"op": "config_get", "name": "TEST"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, "val1")

    def test_jac_api_create_config_nonadmin_fails(self):
        """Test API for creating a config"""
        payload = {"op": "config_set", "name": "EMAIL_HOST_USER", "value": "val1"}
        res = self.notadminc.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_jac_api_create_config_list(self):
        """Test API for creating a config"""
        payload = {
            "op": "config_set",
            "name": "EMAIL_HOST_USER",
            "value": "val1",
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {
            "op": "config_set",
            "name": "EMAIL_HOST_PASSWORD",
            "value": "val2",
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {
            "op": "config_set",
            "name": "EMAIL_DEFAULT_FROM",
            "value": "val3",
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {
            "op": "config_set",
            "name": "EMAIL_BACKEND",
            "value": "val4",
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {"op": "config_list"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertIn("EMAIL_DEFAULT_FROM", res.data)
