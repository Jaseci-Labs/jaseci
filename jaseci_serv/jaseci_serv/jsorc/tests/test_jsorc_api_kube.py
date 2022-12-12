from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from jaseci.utils.utils import TestCaseHelper
from jaseci_serv.utils.test_utils import skip_without_kube
from django.test import TestCase
from jaseci_serv.svc import MetaService

import json


class JsorcAPIKubeTests(TestCaseHelper, TestCase):
    """
    Test the JSORC APIs, that require kubernetes
    """

    def setUp(self):
        super().setUp()
        self.meta = MetaService()
        # Need to reset the MetaService to load in MetaConfig
        # because DB is reset between test
        self.meta.reset()

        self.user = get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.master = self.user.get_master()

        self.nonadmin = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.notadminc = APIClient()
        self.notadminc.force_authenticate(self.nonadmin)

        # Enable JSORC
        self.enable_jsorc()

    def enable_jsorc(self):
        payload = {"op": "config_get", "name": "META_CONFIG", "do_check": False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        meta_config = json.loads(res.data)
        meta_config["automation"] = True
        meta_config["keep_alive"] = []

        # Set automation to be true
        payload = {
            "op": "config_set",
            "name": "META_CONFIG",
            "value": meta_config,
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "service_refresh", "name": "meta"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

    def tearDown(self):
        super().tearDown()

    @skip_without_kube
    def test_jsorc_kube_api_example(self):
        """Example test for jsorc API that relies on kuberentes"""
        pass
