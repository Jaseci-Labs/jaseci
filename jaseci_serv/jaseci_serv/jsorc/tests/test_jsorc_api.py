from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from jaseci.utils.test_core import skip_without_redis


class JsorcAPITests(TestCaseHelper, TestCase):
    """
    Test the JSORC APIs
    """

    def setUp(self):
        super().setUp()
        # First user is always super,
        self.user = get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @skip_without_redis
    def test_service_refresh(self):
        """Test service refresh through the service_refresh API"""
        payload = {"op": "service_refresh", "name": "redis"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["success"])
