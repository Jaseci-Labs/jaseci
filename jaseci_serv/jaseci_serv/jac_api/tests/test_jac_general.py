import base64

from django.contrib.auth import get_user_model
from django.urls import reverse
from jaseci.utils.test_core import skip_without_redis

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

import uuid
import os


class JacGeneralTests(TestCaseHelper, TestCase):
    """Test the publicly available node API"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()

    def quick_call(self, bywho, ops):
        return bywho.post(reverse(f'jac_api:{ops["op"]}'), ops, format="json")

    def test_here_update_fix(self):
        testfile = open(os.path.dirname(__file__) + "/general.jac").read()
        self.quick_call(
            self.client, {"op": "sentinel_register", "name": "test", "code": testfile}
        )

        self.user._h.clear_cache()
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "here_fix_create"}
        )
        self.user._h.clear_cache()
        ret = self.quick_call(
            self.client,
            {
                "op": "walker_run",
                "name": "here_fix_update",
                "nd": ret.data["report"][0],
            },
        )
        self.user._h.clear_cache()
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "here_fix_check"}
        )
        self.user._h.clear_cache()
        self.assertEqual(ret.data["report"], [{"value": "Test"}])

    def test_object_bug(self):
        testfile = open(os.path.dirname(__file__) + "/object_bug.jac").read()
        self.quick_call(
            self.client, {"op": "sentinel_register", "name": "test", "code": testfile}
        )
        self.user._h.clear_cache()
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "test_walk"})
        self.assertEqual(ret.data["success"], True)
        self.user._h.clear_cache()
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "test_walk"})
        self.assertEqual(ret.data["success"], True)
        self.user._h.clear_cache()
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "test_walk"})
        self.assertEqual(ret.data["success"], True)
