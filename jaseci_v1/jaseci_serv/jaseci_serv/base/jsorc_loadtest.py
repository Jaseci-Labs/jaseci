import os
import time
from django.contrib.auth import get_user_model
from django.urls import reverse
import json
from rest_framework.test import APIClient

from time import sleep
from jaseci.utils.utils import logger

APP_PATH = os.path.join(os.path.dirname(__file__), "example_jac")


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

    def run_test(
        self, experiment, mem, policy, experiment_duration, eval_phase, perf_phase
    ):
        """
        Run the corresponding jsorc test
        """
        test_func = getattr(self, self.test)
        if experiment == "":
            return test_func()
        else:
            return test_func(
                experiment, mem, policy, experiment_duration, eval_phase, perf_phase
            )

    def load_action(self, name, mode, wait_for_ready=False):
        """
        Load action in corresponding mode.
        If wait is True, this function will block until the action is fully loaded,
        including microserivice is up and connected etc.
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
        payload = {"op": "jsorc_trackact_start"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def stop_actions_tracking(self):
        payload = {"op": "jsorc_trackact_stop"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def load_action_config(self, action_pkg, action_module):
        """ """
        payload = {
            "op": "jsorc_actions_config",
            "config": action_pkg,
            "name": action_module,
        }
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        return res.data

    def synthetic_apps(
        self, experiment, mem, policy, experiment_duration, eval_phase, perf_phase
    ):
        """
        Run synthetic application
        Available applications are in jaseci_serv/base/example_jac
        """
        try:
            results = {}
            node_mem = [int(mem) * 1024]
            apps = [experiment]
            policies = [policy]
            app_to_actions = {
                "zeroshot_faq_bot": ["jac_nlp.text_seg", "jac_nlp.use_qa"],
                "sentence_pairing": ["jac_nlp.sbert_sim", "jac_nlp.bi_enc"],
                "discussion_analysis": ["jac_nlp.bi_enc", "jac_nlp.cl_summer"],
                "flight_chatbot": ["jac_nlp.use_qa", "jac_nlp.ent_ext"],
                "restaurant_chatbot": ["jac_nlp.bi_enc", "jac_nlp.tfm_ner"],
                "virtual_assistant": [
                    "jac_nlp.text_seg",
                    "jac_nlp.bi_enc",
                    "jac_nlp.tfm_ner",
                    "jac_nlp.sbert_sim",
                    "jac_nlp.use_qa",
                ],
                "flow_analysis": [
                    "jac_nlp.text_seg",
                    "jac_nlp.tfm_ner",
                    "jac_nlp.use_enc",
                ],
                "weather_and_time_assitance": [
                    "jac_speech.vc_tts",
                    "jac_speech.stt",
                    "jac_nlp.bi_enc",
                ],
            }

            for app in apps:
                jac_file = os.path.join(APP_PATH, f"{app}.jac")
                self.sentinel_register(jac_file)
                action_modules = app_to_actions[app]
                for policy in policies:
                    if policy == "all_local" or policy == "all_remote":
                        policy_params = [{}]
                    else:
                        policy_params = [{"node_mem": nm} for nm in node_mem]
                    for pparams in policy_params:
                        pparams["eval_phase"] = eval_phase
                        pparams["perf_phase"] = perf_phase
                        if policy == "all_local":
                            jsorc_policy = "Default"
                            for module in action_modules:
                                package, module = module.split(".")
                                self.load_action_config(f"{package}.config", module)
                                self.load_action(module, "local", wait_for_ready=True)
                        elif policy == "all_remote":
                            jsorc_policy = "Default"
                            for module in action_modules:
                                package, module = module.split(".")
                                self.load_action_config(f"{package}.config", module)
                                self.load_action(module, "remote", wait_for_ready=True)
                        elif policy == "evaluation":
                            jsorc_policy = "Evaluation"
                            # For JSORC mode, we start as remote everything
                            for module in action_modules:
                                package, module = module.split(".")
                                self.load_action_config(f"{package}.config", module)
                                self.load_action(module, "remote", wait_for_ready=True)
                        else:
                            logger.error(f"Unrecognized policy {policy}")
                            return

                        self.set_jsorc_actionpolicy(jsorc_policy, policy_params=pparams)
                        #
                        # Experiment Start
                        #
                        self.start_benchmark()
                        self.start_actions_tracking()
                        start_ts = time.time()
                        while (time.time() - start_ts) < experiment_duration:
                            res = self.run_walker(app)
                        result = self.stop_benchmark()
                        action_result = self.stop_actions_tracking()
                        if policy == "all_local" or policy == "all_remote":
                            policy_str = policy
                        else:
                            policy_str = f"{policy}-mem-{pparams['node_mem']}"
                        results.setdefault(app, {})[policy_str] = {
                            "walker_level": result,
                            "action_level": action_result,
                        }
                        #
                        # Experiment Ends. Unload actions. Reset the cluster
                        #
                        if policy == "all_local":
                            for module in action_modules:
                                package, module = module.split(".")
                                self.unload_action(
                                    module, mode="local", retire_svc=True
                                )
                        elif policy == "all_remote":
                            for module in action_modules:
                                package, module = module.split(".")
                                self.unload_action(
                                    module, mode="remote", retire_svc=True
                                )
                        else:
                            for module in action_modules:
                                package, module = module.split(".")
                                self.unload_action(module, mode="auto", retire_svc=True)
                        sleep(10)
            self.set_jsorc_actionpolicy("Default", policy_params={})
            path = "/root/.jaseci/models/exp_results/"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}/{app}_{policy}.json", "w") as fp:
                json.dump(results, fp)
            return results
        except Exception as e:
            return f"Exception: {e}"
