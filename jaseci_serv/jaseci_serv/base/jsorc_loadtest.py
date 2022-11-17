from django.contrib.auth import get_user_model
from django.urls import reverse
from jaseci.utils.utils import logger

from rest_framework.test import APIClient

import os
import json
from time import sleep
import time

JAC_PATH = os.path.join(os.path.dirname(__file__), "action_micro_jac/")
HLP_JAC_PATH = os.path.join(os.path.dirname(__file__), "hlp_jac/")
APP_PATH = os.path.join(os.path.dirname(__file__), "synthetic_apps")


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

    def run_test(self, experiment):
        """
        Run the corresponding jsorc test
        """
        logger.info("in test")
        test_func = getattr(self, self.test)
        if experiment == "":
            return test_func()
        else:
            return test_func(experiment)

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

    def set_jsorc_actionpolicy(self, policy_name):
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": policy_name}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

    def synthetic_apps(self):
        """
        Run synthetic application
        """
        results = {}
        apps = [
            # "zeroshot_faq_bot",
            # "sentence_pairing"
            "discussion_analysis"
        ]
        app_to_actions = {
            "zeroshot_faq_bot": ["text_seg", "use_qa"],
            "sentence_pairing": ["use_enc", "bi_enc"],
            "discussion_analysis": ["bi_enc", "cl_summer"],
        }
        policies = ["evaluation"]
        # policies = ["all_local"]
        # policies = ["all_evaluation"]
        # policies = ["all_remote", "all_local", "evaluation"]
        for app in apps:
            jac_file = os.path.join(APP_PATH, f"{app}.jac")
            self.sentinel_register(jac_file)
            action_modules = app_to_actions[app]
            for policy in policies:
                if policy == "all_local":
                    jsorc_policy = "Default"
                    for module in action_modules:
                        self.load_action(module, "local", wait_for_ready=True)
                elif policy == "all_remote":
                    jsorc_policy = "Default"
                    for module in action_modules:
                        self.load_action(module, "remote", wait_for_ready=True)
                elif policy == "evaluation":
                    jsorc_policy = "Evaluation"
                    # For JSORC mode, we start as remote everything
                    for module in action_modules:
                        self.load_action(module, "remote", wait_for_ready=True)
                else:
                    logger.error(f"Unrecognized policy {policy}")
                    return

                self.set_jsorc_actionpolicy(jsorc_policy)
                #
                # Experiment Start
                #
                self.start_benchmark()
                self.start_actions_tracking()
                start_ts = time.time()
                experiment_duration = 2 * 60
                while (time.time() - start_ts) < experiment_duration:
                    res = self.run_walker(app)
                result = self.stop_benchmark()
                action_result = self.stop_actions_tracking()
                results.setdefault(app, {})[policy] = {
                    "walker_level": result,
                    "action_level": action_result,
                }
                #
                # Experiment Ends. Unload actions. Reset the cluster
                #
                for module in action_modules:
                    self.unload_action(module, mode="auto", retire_svc=True)
                sleep(10)
        return results

    def action_level_test(self):
        """
        Run action level tests
        """
        performance = {}
        for action_set in [
            # "use_enc",
            # "use_qa",
            "text_seg",
            # "flair_ner",
            # "cl_summer",
            # "bi_enc",
            "tfm_ner",
        ]:
            # for action_set in ["use_enc"]:
            performance[action_set] = {}
            # for mode in ["local", "remote"]:
            for mode in ["remote", "local"]:
                self.load_action(action_set, mode, wait_for_ready=True)
                action_set_path = os.path.join(JAC_PATH, f"{action_set}/")
                for jac_file in os.listdir(action_set_path):
                    # if jac_file != "cos_sim_score.jac":
                    #     continue
                    if not jac_file.endswith(".jac"):
                        continue
                    action_name = jac_file.split(".")[0]
                    if action_name not in performance[action_set]:
                        performance[action_set][action_name] = {}
                    full_jac_file_path = os.path.join(action_set_path, jac_file)
                    jac_code = open(full_jac_file_path).read()
                    payload = {"op": "sentinel_register", "code": jac_code}
                    res = self.sauth_client.post(
                        reverse(f'jac_api:{payload["op"]}'), payload, format="json"
                    )
                    payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Default"}
                    res = self.sauth_client.post(
                        reverse(f'jac_api:{payload["op"]}'), payload, format="json"
                    )
                    self.start_benchmark()
                    self.start_actions_tracking()
                    for i in range(50):
                        res = self.run_walker(action_name)
                    result = self.stop_benchmark()
                    action_result = self.stop_actions_tracking()
                    performance[action_set][action_name][mode] = {
                        "walker_level": result["walker_run"][action_name],
                        "action_level": action_result[-1]["actions_calls"],
                    }
                res = self.unload_action(action_set, mode, retire_svc=True)
                sleep(10)

        for action_set, res in performance.items():
            for action_name, action_perf in res.items():
                action_perf["remote_over_local"] = {}
                for metric in action_perf["local"]["walker_level"].keys():
                    action_perf["remote_over_local"][metric] = (
                        action_perf["remote"]["walker_level"][metric]
                        / action_perf["local"]["walker_level"][metric]
                    )
        return performance

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
        self.start_actions_tracking()

        # Execute the walker trace
        for i in range(1):
            for req in metadata["walkers"]:
                payload = {"op": "walker_run", "name": req["name"], "ctx": req["ctx"]}
                self.sauth_client.post(
                    reverse(f'jac_api:{payload["op"]}'), payload, format="json"
                )

        result["performance"] = self.stop_benchmark()
        result["actions_history"] = self.stop_actions_tracking()
        return result

    def five_modules_experiment(self, experiment="all_local"):
        result = {}
        jac_file = open(JAC_PATH + "five_mixture.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        if experiment == "all_local":
            for action in ["use_enc", "bi_enc", "text_seg", "ent_ext", "cl_summer"]:
                self.load_action(action, "local")
            payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Default"}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
        elif experiment == "all_remote":
            for action in ["use_enc", "bi_enc", "ent_ext", "cl_summer"]:
                self.load_action(action, "remote")
            payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Default"}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
        elif experiment == "evaluate":
            for action in ["use_enc", "bi_enc", "ent_ext", "cl_summer"]:
                self.load_action(action, "local")
            payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Evaluation"}
            res = self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        # # Load use_enc local action
        # payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "local"}
        # res = self.sauth_client.post(
        #     reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        # )
        # # Load bi_enc local action
        # payload = {"op": "jsorc_actions_load", "name": "bi_enc", "mode": "local"}
        # self.sauth_client.post(
        #     reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        # )
        # payload = {"op": "jsorc_actions_load", "name": "bi_enc", "mode": "local"}
        # self.sauth_client.post(
        #     reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        # )
        # Set the policy

        # Start the benchmark
        self.start_benchmark()
        self.start_actions_tracking()

        # Execute the walker
        for i in range(500):
            for walker in [
                "infer",
                "cos_sim_score",
                "get_segments",
                "entity_detection",
                "summarize",
            ]:
                self.run_walker(walker, ctx={})
            # payload = {"op": "walker_run", "name": "cos_sim_score"}
            # self.sauth_client.post(
            #     reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            # )
            # payload = {"op": "walker_run", "name": "infer"}
            # self.sauth_client.post(
            #     reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            # )

        result["performance"] = self.stop_benchmark()
        result["actions_history"] = self.stop_actions_tracking()
        return result

    def two_modules_evaluate(self):
        result = {}
        jac_file = open(JAC_PATH + "mixture.jac").read()
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
        # Load bi_enc local action
        payload = {"op": "jsorc_actions_load", "name": "bi_enc", "mode": "local"}
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
        self.start_actions_tracking()

        # Execute the walker
        for i in range(100):
            payload = {"op": "walker_run", "name": "cos_sim_score"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            payload = {"op": "walker_run", "name": "infer"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result["performance"] = self.stop_benchmark()
        result["actions_history"] = self.stop_actions_tracking()
        return result

    def two_modules_all_local(self):
        result = {}
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

        jac_file = open(JAC_PATH + "mixture.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Default"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start the benchmark
        self.start_benchmark()
        self.start_actions_tracking()

        # Execute the walker
        for i in range(500):
            payload = {"op": "walker_run", "name": "cos_sim_score"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            payload = {"op": "walker_run", "name": "infer"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result["performance"] = self.stop_benchmark()
        result["actions_history"] = self.stop_actions_tracking()
        return result

    def two_modules_all_remote(self):
        result = {}
        jac_file = open(JAC_PATH + "mixture.jac").read()
        # Regsiter the sentinel
        payload = {"op": "sentinel_register", "code": jac_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Set the policy
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Default"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load use_enc local action
        payload = {"op": "jsorc_actions_load", "name": "use_enc", "mode": "remote"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load bi_enc local action
        payload = {"op": "jsorc_actions_load", "name": "bi_enc", "mode": "remote"}
        self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Start the benchmark
        self.start_benchmark()
        self.start_actions_tracking()

        # Execute the walker
        for i in range(10):
            payload = {"op": "walker_run", "name": "cos_sim_score"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            payload = {"op": "walker_run", "name": "infer"}
            self.sauth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )

        result["performance"] = self.stop_benchmark()
        result["actions_history"] = self.stop_actions_tracking()
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
