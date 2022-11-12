import base64
from time import sleep

from django.contrib.auth import get_user_model
from django.urls import reverse
from jaseci_serv.utils.test_utils import skip_without_redis
from jaseci.utils.utils import logger

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

import uuid
import pprint
import os

JAC_PATH = os.path.join(os.path.dirname(__file__), "action_micro_jac/")


class JsorcLoadTest:
    """Test the JSORC APIs"""

    def __init__(self):
        self.client = APIClient()
        try:
            get_user_model().objects.create_user(
                "throwawayJSCITfdfdEST_test@jaseci.com", "password"
            )
            self.user = get_user_model().objects.create_user(
                "JSCITfdfdEST_test@jaseci.com", "password"
            )
            self.suser = get_user_model().objects.create_superuser(
                "JSCITfdfdEST_test2@jaseci.com", "password"
            )
        except Exception as e:
            logger.info("Test set up exception", str(e))
            self.user = get_user_model().objects.filter(
                email="JSCITfdfdEST_test@jaseci.com"
            )
            self.suser = get_user_model().objects.filter(
                email="JSCITfdfdEST_test2@jaseci.com"
            )

        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user)
        self.sauth_client = APIClient()
        self.sauth_client.force_authenticate(self.suser)

    def test_use_enc_cosine_sim_switching(self):
        jac_file = open(JAC_PATH + "use_enc/cos_sim_score.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Load use_enc local action
        payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "local"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start benchmark
        payload = {"op": "jsorc_benchmark_start"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(100):
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        # Stop benchmark and get report
        payload = {"op": "jsorc_benchmark_stop", "report": True}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        print("=================Local Action==============")
        pprint.pprint(res.data, indent=2)

        # Load use_enc remote action
        payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "remote"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        while True:
            payload = {"op": "jsorc_actions_status", "name": "use_enc"}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            if res.data["action_status"]["mode"] == "remote":
                break

            sleep(5)

        # Start benchmark
        payload = {"op": "jsorc_benchmark_start"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(100):
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        # Stop benchmark and get report
        payload = {"op": "jsorc_benchmark_stop", "report": True}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        print("=================Local Action==============")
        pprint.pprint(res.data, indent=2)
