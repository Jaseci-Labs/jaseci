from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import logger
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
        # TODO: why this has to be called explictly?
        self.meta = MetaService(run_svcs=True)

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

        # Enable JSORC
        print("WHAT IS GOING ON")
        logger.info("WHAT IS GOING ON")
        res = self.enable_jsorc()

    def enable_jsorc(self):
        # Get current meta config
        payload = {"op": "config_get", "name": "META_CONFIG"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        meta_config = json.loads(res.data)
        meta_config["automation"] = True

        # Set automation to be true
        payload = {"op": "config_set", "name": "META_CONFIG", "value": meta_config}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Refresh service
        payload = {"op": "service_refresh", "name": "meta"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        return res

    def tearDown(self):
        super().tearDown()

    @skip_without_kube
    def test_jsorc_kube_api_example(self):
        """Test service refresh through the service_refresh API"""
        print("test_jsorc_kube_api_example")
