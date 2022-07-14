from django.contrib.auth import get_user_model
from django.urls import reverse

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from jaseci_serv.base.models import JaseciObject, GlobalVars


data = {}


class TestSocialAuth(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()
