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
            'throwawayJSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.nonadmin = get_user_model().objects.create_user(
            'JSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.notadminc = APIClient()
        self.notadminc.force_authenticate(self.nonadmin)
        self.master = self.user.get_master()

    def tearDown(self):
        super().tearDown()

    def test_jac_api_create_config(self):
        """Test API for creating a config"""
        payload = {'op': 'config_set', 'name': 'test1', 'value': 'val1'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {'op': 'config_get', 'name': 'test1'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "val1")

    def test_jac_api_create_config_nonadmin_fails(self):
        """Test API for creating a config"""
        payload = {'op': 'config_set', 'name': 'test1', 'value': 'val1'}
        res = self.notadminc.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_jac_api_create_config_list(self):
        """Test API for creating a config"""
        payload = {'op': 'config_set', 'name': 'test1', 'value': 'val1'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {'op': 'config_set', 'name': 'test2', 'value': 'val2'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {'op': 'config_set', 'name': 'test3', 'value': 'val3'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {'op': 'config_set', 'name': 'test4', 'value': 'val4'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = {'op': 'config_list'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.data[2], 'test3')
