from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from jaseci_serv.svc import MetaService


class JsorcAPITests(TestCaseHelper, TestCase):
    """
    Test the JSORC APIs
    """

    def setUp(self):
        super().setUp()
        self.meta = MetaService()
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

    def test_service_refresh(self):
        """Test service refresh through the service_refresh API"""
        payload = {"op": "service_refresh", "name": "meta", "do_check": False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["success"])
