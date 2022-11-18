from jaseci.svc.actions_optimizer.configs import ACTION_CONFIGS
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.utils.utils import logger
from jaseci.svc.kubernetes import Kube
from jaseci.svc.actions_optimizer.actions_state import ActionsState
from jaseci.actions.live_actions import (
    load_module_actions,
    unload_module,
    unload_remote_actions,
    load_remote_actions,
    live_actions,
)
import requests
import time
from kubernetes.client.rest import ApiException

POLICIES = ["Default", "BackAndForth", "Evaluation"]


class ActionsOptimizer:
    def __init__(
        self,
        kube: Kube,
        policy: str = "Default",
        benchmark: dict = {},
        actions_history: dict = {},
        actions_calls: dict = {},
        namespace: str = "default",
    ) -> None:
        self.kube = kube
        self.policy = policy
        self.actions_state = ActionsState()
        self.actions_change = {}
        self.policy_state = {}
        self.benchmark = benchmark
        self.jsorc_interval = 0
        self.actions_history = actions_history
        self.actions_calls = actions_calls
        self.namespace = namespace

    def set_action_policy(self, policy_name: str):
        """
        Set the action optimization policy for JSORC
        """
        # TODO: manage policy switching if there are unresolved actions state
        if policy_name in POLICIES:
            self.policy = policy_name
            self.policy_state[policy_name] = {}
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
        logger.info("=====JSORC RUN=======")
        if self.policy == "Default":
            # Default policy does not manage action automatically
            return
        elif self.policy == "BackAndForth":
            self._actionpolicy_backandforth()
        elif self.policy == "Evaluation":
            self._actionpolicy_evaluation()
        elif self.policy == "ActionEvaluation":
            self._actionpolicy_actionevaluation()

        if len(self.actions_change) > 0:
            self.apply_actions_change()

    def _actionpolicy_backandforth(self):
        """
        A policy mostly for testing purpose.
        It will switch one action module back and forth between local and remote at a fixed interval
        """
        policy_state = self.policy_state["BackAndForth"]
        if len(policy_state) == 0:
            # initialize policy tracking state
            policy_state = {"time_since_switch": 0, "actions_to_switch": "use_enc"}

        # Check if its time to switch again
        policy_state["time_since_switch"] += self.jsorc_interval

        if policy_state["time_since_switch"] >= 9:
            # Check if the action is still switching
            if policy_state["actions_to_switch"] in self.actions_change:
                return

            action_name = policy_state["actions_to_switch"]
            cur_state = self.actions_state.get_state(action_name)
            if cur_state is None:
                cur_state = self.actions_state.init_state(action_name)

            if cur_state["mode"] is None:
                # start with local
                self.actions_change[action_name] = "to_local"
            elif cur_state["mode"] == "local" or cur_state["mode"] == "module":
                self.actions_change[action_name] = "local_to_remote"
            elif cur_state["mode"] == "remote":
                self.actions_change[action_name] = "remote_to_local"

            policy_state["time_since_switch"] = 0
        self.policy_state["BackAndForth"] = policy_state

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
                "eval_phase": 10,  # how long is evaluatin period (in seconds)
                "perf_phase": 100,  # how long is the performance period (in seconds)
                "cur_phase": 0,  # how long the current period has been running
            }
        policy_state["cur_phase"] += self.jsorc_interval

        # check if we should go into evaluation phase
        if (
            policy_state["phase"] == "perf"
            and policy_state["cur_phase"] >= policy_state["perf_phase"]
        ):
            logger.info("===Evaluation Policy=== Switching to evaluation mode")
            policy_state["phase"] = "eval"
            policy_state["cur_phase"] = 0
            policy_state["cur_config"] = None
            if len(policy_state["remain_configs"]) == 0:
                logger.info("===Evaluation Policy=== Initialize evaluation model")
                # Initialize configs to eval
                actions = self.actions_state.get_active_actions()
                # construct list of possible configurations
                all_configs = [{}]
                for act in actions:
                    new_configs = []
                    for c in all_configs:
                        for m in ["local", "remote"]:
                            c[act] = m
                            new_configs.append(dict(c))
                    all_configs = list(new_configs)
                policy_state["remain_configs"] = all_configs

        if policy_state["phase"] == "eval":
            # In evaluation phase
            if policy_state["cur_config"] is None:
                logger.info("===Evaluation Policy=== First evaluation config")
                logger.info("===Evaluation Policy=== Initialize evaluation model")
                # Initialize configs to eval
                actions = self.actions_state.get_active_actions()
                # construct list of possible configurations
                all_configs = [{}]
                for act in actions:
                    new_configs = []
                    for c in all_configs:
                        for m in ["local", "remote"]:
                            c[act] = m
                            new_configs.append(dict(c))
                    all_configs = list(new_configs)
                policy_state["remain_configs"] = all_configs

                # This is the start of evaluation period
                policy_state["cur_config"] = policy_state["remain_configs"][0]
                del policy_state["remain_configs"][0]
                policy_state["cur_phase"] = 0
                self.benchmark["active"] = True
                self.actions_change = self._get_action_change(
                    policy_state["cur_config"]
                )
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
                        policy_state["phase"] = "perf"
                        policy_state["cur_config"] = None
                        policy_state["past_configs"] = []
                        policy_state["cur_phase"] = 0
                        self.benchmark["requests"] = {}
                        self.benchmark["active"] = False
                        logger.info(
                            f"===Evaluation Policy=== Evaluation phase over. Selected best config as {best_config}"
                        )
                    else:
                        next_config = policy_state["remain_configs"][0]
                        del policy_state["remain_configs"][0]
                        self.actions_change = self._get_action_change(next_config)
                        # TODO: for now, we are including the configuration switching part in the eval period for simplicity
                        policy_state["cur_config"] = next_config
                        policy_state["cur_phase"] = 0
                        self.benchmark["active"] = True
                        self.benchmark["requests"] = {}
                        logger.info(
                            f"===Evaluation Policy=== Switching to next config to evaluate {next_config}"
                        )

        self.policy_state["Evaluation"] = policy_state

    def _actionpolicy_actionevaluation(self):
        """
        Use action pressure to trigger an evaluation
        """
        policy_state = self.policy_state["ActionEvaluation"]
        if len(policy_state) == 0:
            # Initialize the policy tracking state
            policy_state = {}

    def _actionpolicy_actionprediction(self):
        """
        use action pressure to predict the next configuration
        """
        pass

    def _get_action_change(self, new_action_state):
        """
        Given a new desired action state and the current action_state tracking, return the change set
        """
        change_state = {}
        for name, new_state in new_action_state.items():
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
            if change_type == "to_local" or change_type == "to_module":
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

    def kube_create(self, config):
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            try:
                self.kube.create(kind, self.namespace, conf)
            except ApiException:
                logger.error(f"Error creating {kind} for {name}")

    def kube_delete(self, config):
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            try:
                logger.info(
                    f"ActionsOptimzer: deleting {kind} for {name} for namespace {self.namespace}"
                )
                self.kube.delete(kind, name, self.namespace)
            except ApiException as e:
                logger.error(
                    f"Error deleting {kind} for {name} for namespace {self.namespace}"
                )
                logger.error(str(e))

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
        TODO
        """
        config = ACTION_CONFIGS[name]["remote"]
        self.kube_delete(config)
        self.actions_state.remove_remote(name)

    def spawn_remote(self, name):
        """
        Spawn a microservice through the kube service
        TODO
        """
        config = ACTION_CONFIGS[name]["remote"]
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
        if name == "tfm_ner":
            # tfm_ner requires an initial model loading
            self.call_action(
                "tfm_ner.load_model", "/trained_models/trained_tfm_ner_model/", True
            )

    def load_action_remote(self, name, unload_existing=False):
        """
        Load a remote action.
        JSORC will get the URL of the remote microservice and stand up a microservice if there isn't currently one in the cluster.
        Return True if the remote action is loaded successfully,
        False otherwise
        """
        logger.info(f"==Actions Optimizer== LOAD remote action for {name}")
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
            logger.info(f"==Actions Optimizer== LOADED remote action for {name}")
            return True

        return False

    def load_action_module(self, name, unload_existing=False):
        """
        Load an action module
        """
        logger.info(f"==Actions Optimizer== LOAD module action for {name}")
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            logger.info("==Actions Optimizer== initialize actions_state")
            cur_state = self.actions_state.init_state(name)

        if cur_state["mode"] == "module":
            logger.info(f"==Actions Optimizer== {name} already loaded as module")
            # Check if there is already a local action loaded
            return

        module = ACTION_CONFIGS[name]["module"]
        if unload_existing:
            logger.info("==Actions Optimizer== unloading existing remote action {name}")
            self.unload_action_remote(name)
        load_module_actions(module)
        self.action_prep(name)
        self.actions_state.module_action_loaded(name, module)
        logger.info(f"==Actions Optimizer== LOADED module action for {name}")

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

        # Hack?
        module_name = module_name.split(".")[-1]
        module_name = f"jaseci_ai_kit.modules.{module_name}.{module_name}"

        unload_module(module_name)
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
