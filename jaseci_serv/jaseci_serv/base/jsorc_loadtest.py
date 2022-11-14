from django.contrib.auth import get_user_model
from django.urls import reverse
from jaseci.utils.utils import logger

from rest_framework.test import APIClient

import os
import json
from time import sleep

JAC_PATH = os.path.join(os.path.dirname(__file__), "action_micro_jac/")
HLP_JAC_PATH = os.path.join(os.path.dirname(__file__), "hlp_jac/")


class JsorcLoadTest:
    """
    A load tester module around JSORC.
    """

    def __init__(self, test):
        self.client = APIClient()
        user_email = "JSCITfdfdEST_test@jaseci.com"
        suser_email = "JSCITfdfdEST_test2@jaseci.com"
        password = "password"
        try:
            self.user = get_user_model().objects.get(email=user_email.lower())
        except get_user_model().DoesNotExist:
            self.user = get_user_model().objects.create_user(user_email, password)
        try:
            self.suser = get_user_model().objects.get(email=suser_email.lower())
        except get_user_model().DoesNotExist:
            self.suser = get_user_model().objects.create_superuser(
                suser_email, password
            )

        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user)
        self.sauth_client = APIClient()
        self.sauth_client.force_authenticate(self.suser)

        self.test = test

    def run_test(self):
        """
        Run the corresponding jsorc test
        """
        test_func = getattr(self, self.test)
        return test_func()

    def hlp_evaluate(self):
        result = {}
        # Regsiter the sentinel
        jac_file = open(HLP_JAC_PATH + "main.jir").read()
        payload = {"op": "sentinel_register", "code": jac_file, "mode": "ir"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        with open(HLP_JAC_PATH + "metadata.json") as fin:
            metadata = json.load(fin)

        for action in metadata["actions"]:
            payload = {"op": "jsorc_actions_load", "name": action, "mode": "local"}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        for req in metadata["prep"]:
            payload = {"op": "walker_run", "name": req["name"], "ctx": req["ctx"]}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Evaluation"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start the benchmark
        self.start_benchmark()

        # Execute the walker trace
        for i in range(200):
            for req in metadata["walkers"]:
                payload = {"op": "walker_run", "name": req["name"], "ctx": req["ctx"]}
                self.sauth_client.post(
                    reverse(f'jac_api:{payload["op"]}'), payload, format="json"
                )

        result = self.stop_benchmark()
        return result

    def two_modules_evaluate(self):
        result = {}
        jac_file = open(JAC_PATH + "use_enc_and_bi_enc.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Evaluation"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load use_enc local action
        payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "local"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load bi_enc local action
        payload = {"op": "jsorc_actions_load", "name": "bi_enc", "mode": "local"}
        self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start the benchmark
        self.start_benchmark()

        # Execute the walker
        for i in range(200):
            payload = {"op": "walker_run", "name": "cos_sim_score"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            payload = {"op": "walker_run", "name": "infer"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result = self.stop_benchmark()
        return result

    def use_enc_evaluate(self):
        result = {}
        jac_file = open(JAC_PATH + "use_enc/cos_sim_score.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Evaluation"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load use_enc local action
        payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "local"}

        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start the benchmark
        self.start_benchmark()

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(200):
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result = self.stop_benchmark()
        return result

    def use_enc_back_and_forth(self):
        result = {}
        jac_file = open(JAC_PATH + "use_enc/cos_sim_score.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "BackAndForth"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Start the benchmark
        self.start_benchmark()

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(200):
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result = self.stop_benchmark()
        return result

    def start_benchmark(self):
        # Start benchmark
        payload = {"op": "jsorc_benchmark_start"}
        self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

    def stop_benchmark(self):
        # Stop benchmark and get report
        payload = {"op": "jsorc_benchmark_stop", "report": True}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def use_enc_cosine_sim_switching(self):
        result = {}
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

        self.start_benchmark()

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(20):
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result["local"] = self.stop_benchmark()

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

        self.start_benchmark()

        # Execute the walker
        payload = {"op": "walker_run", "name": "cos_sim_score"}
        for i in range(20):
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        # Stop benchmark and get report
        result["remote"] = self.stop_benchmark()

        return result
