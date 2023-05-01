"""
Module that manage and optimizes the actions configuration of Jaseci
"""
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.kube_svc import KubeService
from jaseci.jsorc.remote_actions import ACTIONS_SPEC_LOC
from jaseci.utils.utils import logger
from jaseci.jsorc.live_actions import (
    load_module_actions,
    unload_module,
    unload_remote_actions,
    load_remote_actions,
    live_actions,
    action_configs,
)

import requests
import copy
import time

from .actions_state import ActionsState

POLICIES = ["Default", "Evaluation"]
THRESHOLD = 0.2
NODE_MEM_THRESHOLD = 0.8


class ActionsOptimizer:
    def __init__(
        self,
        namespace: str = "default",
        policy: str = "Default",
        benchmark: dict = {},
        actions_history: dict = {},
        actions_calls: dict = {},
    ) -> None:
        self.actions_state = ActionsState()
        self.actions_change = {}
        self.jsorc_interval = 0
        self.namespace = namespace
        self.policy = policy
        self.benchmark = benchmark
        self.actions_history = actions_history
        self.actions_calls = actions_calls
        self.policy_params = {}
        self.policy_state = {}
        self.last_eval_configs = []

    def kube_create(self, config):
        kube = JsOrc.svc("kube").poke(cast=KubeService)
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            kube.create(kind, name, conf, kube.namespace, "ActionsOptimzer:")

    def kube_delete(self, config):
        kube = JsOrc.svc("kube").poke(cast=KubeService)
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            kube.delete(kind, name, kube.namespace, "ActionsOptimzer:")

    def get_actions_status(self, name=""):
        """
        Return the state of action
        """
        if name == "":
            return self.actions_state.get_all_state()
        else:
            return self.actions_state.get_state(name)

    def retire_remote(self, name):
        """
        Retire a microservice through the kube service
        """
        config = action_configs[name]["remote"]
        self.kube_delete(config)
        self.actions_state.remove_remote(name)

    def spawn_remote(self, name):
        """
        Spawn a microservice through the kube service
        """
        config = action_configs[name]["remote"]
        self.kube_create(config)
        url = f"http://{config['Service']['metadata']['name']}/"
        return url

    def call_action(self, action_name, *params):
        """
        Call an action via live_actions
        """
        func = live_actions[action_name]
        func(*params)

    def action_prep(self, name):
        """
        Any action preparation that needs to be called right after action is loaded
        """
        pass

    def load_action_remote(self, name, unload_existing=False):
        """
        Load a remote action.
        JSORC will get the URL of the remote microservice
        and stand up a microservice if there isn't currently one in the cluster.
        Return True if the remote action is loaded successfully,
        False otherwise
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            cur_state = self.actions_state.init_state(name)

        if cur_state["mode"] == "remote" and cur_state["remote"]["status"] == "READY":
            # Check if there is already a remote action loaded
            return True

        url = self.actions_state.get_remote_url(name)
        if url is None:
            # Spawn a remote microservice
            url = self.spawn_remote(name)
            self.actions_state.start_remote_service(name, url)
            cur_state = self.actions_state.get_state(name)

        if cur_state["remote"]["status"] == "STARTING":
            if_ready = self.remote_action_ready_check(name, url)
            if if_ready:
                self.actions_state.set_remote_action_ready(name)
                cur_state = self.actions_state.get_state(name)

        if cur_state["remote"]["status"] == "READY":
            if unload_existing:
                self.unload_action_module(name)
            load_remote_actions(url)
            self.action_prep(name)
            self.actions_state.remote_action_loaded(name)
            return True

        return False

    def load_action_module(self, name, unload_existing=False):
        """
        Load an action module
        """
        cur_state = self.actions_state.get_state(name)
        logger.info(cur_state)
        if cur_state is None:
            cur_state = self.actions_state.init_state(name)

        if cur_state["mode"] == "module":
            logger.info("ALREADY A MODULE LOADED")
            # Check if there is already a local action loaded
            return

        if name not in action_configs:
            return

        module = action_configs[name]["module"]
        loaded_module = action_configs[name]["loaded_module"]
        if unload_existing:
            self.unload_action_remote(name)

        load_module_actions(module, loaded_module)
        self.action_prep(name)
        self.actions_state.module_action_loaded(name, module, loaded_module)

    def unload_action_auto(self, name):
        """
        Unload an action based on how it is currently loaded
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            return False, "Action is not loaded."
        if cur_state["mode"] == "module":
            return self.unload_action_module(name)
        elif cur_state["mode"] == "remote":
            return self.unload_action_remote(name)
        return False, f"Unrecognized action loaded status {cur_state['mode']}"

    def unload_action_module(self, name):
        """
        Unload an action module
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            return False, "Action is not loaded."

        if cur_state["mode"] != "module":
            return False, "Action is not loaded as module."

        module_name = cur_state["module"]["name"]
        loaded_module = cur_state["module"]["loaded_module"]

        unload_module(module_name)
        unload_module(loaded_module)
        self.actions_state.module_action_unloaded(name)

        return (True, f"Action module {name} unloaded.")

    def unload_action_remote(self, name):
        """
        Unload a remote action
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            return False, "Action is not loaded."

        if cur_state["mode"] != "remote":
            return False, "Action is not loaded as remote."

        if cur_state["remote"]["status"] != "READY":
            return False, "Remote action is not ready."

        # Get the list of actions from the action spec of the server
        url = cur_state["remote"]["url"]

        unload_remote_actions(url)
        self.actions_state.remote_action_unloaded(name)

        return (True, f"Remote actions from {url} unloaded.")

    def remote_action_ready_check(self, name, url):
        """
        Check if a remote action is ready by querying the action_spec endpoint
        """
        if url is None:
            return False
        spec_url = url.rstrip("/") + ACTIONS_SPEC_LOC
        headers = {"content-type": "application/json"}
        try:
            res = requests.get(spec_url, headers=headers, timeout=1)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            # Remote service not ready yet
            return False

        return res.status_code == 200

    def set_action_policy(self, policy_name: str, policy_params: dict = {}):
        """
        Set the action optimization policy for JSORC
        """
        # TODO: manage policy switching if there are unresolved actions state
        if policy_name in POLICIES:
            self.policy = policy_name
            self.policy_state[policy_name] = {}
            self.policy_params = policy_params
            return True
        else:
            return f"Policy {policy_name} not found."

    def get_action_policy(self):
        """
        Return the currently active action policy
        """
        return self.policy

    def run(self, jsorc_interval: int):
        """
        The main optimization function.
        This gets invoked by JSROC regularly at a configured interval.
        """
        self.jsorc_interval = jsorc_interval
        if self.policy == "Default":
            # Default policy does not manage action automatically
            return
        elif self.policy == "Evaluation":
            self._actionpolicy_evaluation()
        if len(self.actions_change) > 0:
            self.apply_actions_change()

    def _init_evalution_policy(self, policy_state):
        # 999 is just really large memory size so everything can fits in local
        node_mem = self.policy_params.get("node_mem", 999 * 1024)
        jaseci_runtime_mem = self.policy_params.get("jaseci_runtime_mem", 300)
        # Initialize configs to eval
        actions = self.actions_state.get_active_actions()
        # construct list of possible configurations
        all_configs = [{"local_mem": jaseci_runtime_mem}]
        for act in actions:
            new_configs = []
            for con in all_configs:
                for m in ["local", "remote"]:
                    c = copy.deepcopy(con)
                    c[act] = m
                    if m == "local":
                        local_mem_requirement = action_configs[act][
                            "local_mem_requirement"
                        ]
                        c["local_mem"] = c["local_mem"] + local_mem_requirement
                        if c["local_mem"] < (node_mem * NODE_MEM_THRESHOLD):
                            new_configs.append(dict(c))
                        else:
                            logger.info(
                                f"config dropped for memory constraint: {c},\n\tcurrent node memory: {node_mem}\n\tavailable memory: {(node_mem * NODE_MEM_THRESHOLD)-c['local_mem'] }"
                            )
                    else:
                        new_configs.append(dict(c))
            all_configs = list(new_configs)
        policy_state["remain_configs"] = all_configs

    def _actionpolicy_evaluation(self):
        """
        A evaluation based policy.
        JSORC cycle through possible action configurations and evaluate request performance and select the one with the best performance.
        Use the post_request_hook from JSORC to track request performance
        """
        logger.info("===Evaluation Policy===")
        policy_state = self.policy_state["Evaluation"]

        if len(policy_state) == 0:
            # Initialize policy tracking state
            policy_state = {
                "phase": "eval",  # current phase of policy: eval|perf
                "cur_config": None,  # current active configuration
                "remain_configs": [],  # remaining configurations that need to be evaluated
                "past_configs": [],  # configurations already evaluated
                "eval_phase": self.policy_params.get(
                    "eval_phase", 10
                ),  # how long is evaluatin period (in seconds)
                "perf_phase": self.policy_params.get(
                    "perf_phase", 100
                ),  # how long is the performance period (in seconds)
                "cur_phase": 0,  # how long the current period has been running
                "prev_best_config": self.actions_state.get_all_state(),
            }
        policy_state["cur_phase"] += self.jsorc_interval

        # check if we should go into evaluation phase
        if (
            policy_state["phase"] == "perf"
            and policy_state["cur_phase"] >= policy_state["perf_phase"]
        ):
            # if no enough walker were execueted in this period, keep in perf phase
            if "walker_run" not in self.benchmark["requests"]:
                policy_state["cur_phase"] = 0
            else:
                logger.info("===Evaluation Policy=== Switching to evaluation mode")
                policy_state["phase"] = "eval"
                policy_state["cur_phase"] = 0
                policy_state["cur_config"] = None
                if len(policy_state["remain_configs"]) == 0:
                    self._init_evalution_policy(policy_state)
        if policy_state["phase"] == "eval":
            # In evaluation phase
            if policy_state["cur_config"] is None:
                self._init_evalution_policy(policy_state)

                # This is the start of evaluation period
                policy_state["cur_config"] = policy_state["remain_configs"][0]
                del policy_state["remain_configs"][0]
                policy_state["cur_phase"] = 0
                self.benchmark["active"] = True
                self.benchmark["requests"] = {}
                self.actions_change = self._get_action_change(
                    policy_state["cur_config"]
                )
                if len(self.actions_change) > 0:
                    logger.info(
                        f"===Evaluation Policy=== Switching eval config to {policy_state['cur_config']}"
                    )
                    policy_state["phase"] = "eval_switching"
                    self.benchmark["active"] = False
            else:
                if policy_state["cur_phase"] >= policy_state["eval_phase"]:
                    # The eval phase for the current configuration is complete
                    # Get performance
                    if "walker_run" not in self.benchmark["requests"]:
                        # meaning no incoming requests during this period.
                        # stay in this phase
                        logger.info(f"===Evaluation Policy=== No walkers were executed")
                        self.policy_state["Evaluation"] = policy_state
                        return

                    walker_runs = []
                    for walker, times in self.benchmark["requests"][
                        "walker_run"
                    ].items():
                        if walker == "_default_":
                            continue
                        else:
                            walker_runs.extend(times)

                    avg_walker_lat = sum(walker_runs) / len(walker_runs)
                    policy_state["cur_config"]["avg_walker_lat"] = avg_walker_lat
                    policy_state["past_configs"].append(policy_state["cur_config"])
                    logger.info(
                        f"===Evaluation Policy=== Complete evaluation period for {policy_state['cur_config']} latency: {avg_walker_lat}"
                    )

                    # check if all configs have been evaluated
                    if len(policy_state["remain_configs"]) == 0:
                        # best config is the one with the fastest walker latency during the evaluation period
                        logger.info(f"===Evaluation Policy=== Evaluation phase over. ")
                        best_config = min(
                            policy_state["past_configs"],
                            key=lambda x: x["avg_walker_lat"],
                        )
                        # Switch the system to the best config
                        del best_config["avg_walker_lat"]
                        self.actions_change = self._get_action_change(best_config)

                        # ADAPTIVE: if the selected best config is the same config as the previous best one, double the performance period
                        if all(
                            [
                                best_config[act]
                                == policy_state["prev_best_config"][act]["mode"]
                                for act in best_config.keys()
                                if act in action_configs.keys()
                            ]
                        ):
                            policy_state["perf_phase"] *= 2
                            logger.info(
                                f"===Evaluation Policy=== Best config is the same as previous one. Doubling performance phase to {policy_state['perf_phase']}"
                            )

                        policy_state["phase"] = "perf"
                        policy_state["cur_config"] = None
                        policy_state["past_configs"] = []
                        policy_state["cur_phase"] = 0
                        self.benchmark["requests"] = {}
                        self.benchmark["active"] = True
                        logger.info(
                            f"===Evaluation Policy=== Evaluation phase over. Selected best config as {best_config}"
                        )
                    else:
                        next_config = policy_state["remain_configs"][0]
                        del policy_state["remain_configs"][0]
                        self.actions_change = self._get_action_change(next_config)
                        policy_state["cur_config"] = next_config
                        policy_state["cur_phase"] = 0
                        self.benchmark["requests"] = {}
                        if len(self.actions_change) > 0:
                            logger.info(
                                f"===Evaluation Policy=== Switching eval config to {policy_state['cur_config']}"
                            )
                            policy_state["phase"] = "eval_switching"
                            self.benchmark["active"] = False
                        else:
                            policy_state["phase"] = "eval"
                            self.benchmark["active"] = True
                        logger.info(
                            f"===Evaluation Policy=== Switching to next config to evaluate {next_config}"
                        )
        elif policy_state["phase"] == "eval_switching":
            # in the middle of switching between configs for evaluation
            if len(self.actions_change) == 0:
                # this means all actions change have been applied, start evaluation phase
                logger.info(
                    f"===Evaluation Policy=== All actions change have been applied. Start evaluation phase."
                )
                policy_state["phase"] = "eval"
                policy_state["cur_phase"] = 0
                self.benchmark["active"] = True
                self.benchmark["requests"] = {}
        self.policy_state["Evaluation"] = policy_state

    def _get_action_change(self, new_action_state):
        """
        Given a new desired action state and the current action_state tracking, return the change set
        """
        change_state = {}
        for name, new_state in new_action_state.items():
            if name not in action_configs.keys():
                continue
            cur = self.actions_state.get_state(name)
            if cur is None:
                cur = self.actions_state.init_state(name)
            if new_state == "local":
                new_state = "module"
            if new_state != cur["mode"]:
                change_str = (
                    f"{cur['mode'] if cur['mode'] is not None else ''}_to_{new_state}"
                )
                change_state[name] = change_str
        return change_state

    def apply_actions_change(self):
        """
        Apply any action configuration changes
        """
        actions_change = dict(self.actions_change)
        # For now, to_* and *_to_* are the same logic
        # But this might change down the line
        for name, change_type in actions_change.items():
            logger.info(f"==Actions Optimizer== Changing {name} {change_type}")
            if change_type in ["to_local", "_to_local", "_to_module", "to_module"]:
                # Switching from no action loaded to local
                self.load_action_module(name)
                del self.actions_change[name]
            elif change_type == "to_remote":
                loaded = self.load_action_remote(name)
                if loaded:
                    del self.actions_change[name]
            elif change_type == "local_to_remote" or change_type == "module_to_remote":
                # loaded = self.load_action_remote(name, unload_existing=True)
                loaded = self.load_action_remote(name)
                if loaded:
                    del self.actions_change[name]
            elif change_type == "remote_to_local" or change_type == "remote_to_module":
                # self.load_action_module(name, unload_existing=True)
                self.load_action_module(name)
                del self.actions_change[name]

        if len(actions_change) > 0 and self.actions_history["active"]:
            # Summarize action stats during this period and add to previous state
            self.summarize_action_calls()
            self.actions_history["history"].append(
                {"ts": time.time(), "actions_state": self.actions_state.get_all_state()}
            )

    def summarize_action_calls(self):
        actions_summary = {}
        for action_name, calls in self.actions_calls.items():
            actions_summary[action_name] = sum(calls) / len(calls)
        self.actions_calls.clear()

        if len(self.actions_history["history"]) > 0:
            self.actions_history["history"][-1]["actions_calls"] = actions_summary
