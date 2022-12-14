from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from time import sleep


class JsorcLoadTest:
    """
    A load tester module around JSORC.
    TODO: add experiment test cases
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

    def run_test(self, experiment, mem):
        """
        Run the corresponding jsorc test
        """
        test_func = getattr(self, self.test)
        if experiment == "":
            return test_func()
        else:
            return test_func(experiment, mem)

    def load_action(self, name, mode, wait_for_ready=False):
        """
        Load action in corresponding mode.
        If wait is True, this function will block until the action is fully loaded, including microserivice is up and connected etc.
        """
        payload = {"op": "jsorc_actions_load", "name": name, "mode": mode}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        while wait_for_ready:
            mode = "module" if mode == "local" else mode
            if res.data["action_status"]["mode"] == mode:
                break
            sleep(10)
            payload = {"op": "jsorc_actions_load", "name": name, "mode": mode}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

    def unload_action(self, name, mode, retire_svc=False):
        payload = {
            "op": "jsorc_actions_unload",
            "name": name,
            "mode": mode,
            "retire_svc": retire_svc,
        }
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def run_walker(self, walker_name, ctx={}):
        payload = {"op": "walker_run", "name": walker_name, "ctx": ctx}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def sentinel_register(self, jac_file):
        jac_code = open(jac_file).read()
        # TODO: remove this once opt_level bug is fixed
        payload = {"op": "sentinel_register", "code": jac_code, "opt_level": 2}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

    def set_jsorc_actionpolicy(self, policy_name, policy_params):
        payload = {
            "op": "jsorc_actionpolicy_set",
            "policy_name": policy_name,
            "policy_params": policy_params,
        }
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

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

    def start_actions_tracking(self):
        payload = {"op": "jsorc_actionstracking_start"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def stop_actions_tracking(self):
        payload = {"op": "jsorc_actionstracking_stop"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data
