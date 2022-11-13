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
)
import requests
from kubernetes.client.rest import ApiException

POLICIES = ["Default", "BackAndForth"]


class ActionsOptimizer:
    def __init__(self, kube: Kube, policy: str = "Default") -> None:
        self.kube = kube
        self.policy = policy
        self.actions_state = ActionsState()
        self.actions_change = {}
        self.policy_state = {}
        self.jsorc_interval = 0

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
        if self.policy == "Default":
            # Default policy does not manage action automatically
            return
        elif self.policy == "BackAndForth":
            self._actionpolicy_backandforth()

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
        if policy_state["time_since_switch"] >= 60:
            # Check if the action is still switching
            if policy_state["actions_to_switch"] in self.actions_change:
                return

            action_name = policy_state["actions_to_switch"]
            cur_state = self.actions_state.get_state(action_name)
            if cur_state["mode"] is None:
                # start with local
                self.actions_change[action_name] = "to_local"
            elif cur_state["mode"] == "local":
                self.actions_change[action_name] = "local_to_remote"
            elif cur_state["mode"] == "remote":
                self.actions_change[action_name] = "remote_to_local"

    def apply_actions_change(self):
        """
        Apply any action configuration changes
        """
        actions_change = dict(self.actions_change)
        # For now, to_* and *_to_* are teh same logic
        # But this might change down the line
        for name, change_type in actions_change.items():
            if change_type == "to_local":
                # Switching from no action loaded to local
                self.load_action_module(name)
                del self.actions_change[name]
            elif change_type == "to_remote":
                loaded = self.load_action_remote(name)
                if loaded:
                    del self.actions_change[name]
            elif change_type == "local_to_remote":
                loaded = self.load_action_remote(name)
                if loaded:
                    del self.actions_change[name]
            elif change_type == "remote_to_local":
                self.load_action_module(name)
                del self.actions_change[name]

    def kube_create(self, config):
        namespace = "default"  # TODO: hardcoded
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            try:
                self.kube.create(kind, namespace, conf)
            except ApiException:
                logger.error(f"Error creating {kind} for {name}")

    def kube_delete(self, config):
        namespace = "default"  # TODO: hardcoded for now
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            try:
                logger.info(
                    f"ActionsOptimzer: deleting {kind} for {name} for namespace {namespace}"
                )
                self.kube.delete(kind, name, namespace)
            except ApiException as e:
                logger.error(
                    f"Error deleting {kind} for {name} for namespace {namespace}"
                )
                logger.error(str(e))

    def get_actions_status(self, name):
        """
        Return the state of action
        """
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

    def load_action_remote(self, name):
        """
        Load a remote action.
        JSORC will get the URL of the remote microservice and stand up a microservice if there isn't currently one in the cluster.
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
            load_remote_actions(url)
            self.actions_state.remote_action_loaded(name)
            return True

        return False

    def load_action_module(self, name):
        """
        Load an action module
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            cur_state = self.actions_state.init_state(name)

        if cur_state["mode"] == "module":
            # Check if there is already a local action loaded
            return

        module = ACTION_CONFIGS[name]["module"]
        load_module_actions(module)
        self.actions_state.module_action_loaded(name, module)

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
