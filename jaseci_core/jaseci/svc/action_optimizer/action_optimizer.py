from jaseci.svc.action_optimizer.configs import ACTION_CONFIGS
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.utils.utils import logger
from jaseci.svc.kubernetes import Kube
from jaseci.actions.live_actions import (
    load_module_actions,
    unload_module,
    load_remote_actions,
)
import requests
from kubernetes.client.rest import ApiException


class ActionsState:
    def __init__(self):
        """
        Actions state format:
        actions_state = {
            "ACTION_NAME": {
                "mode": "local|remote",
                "remote": {
                    "url": "remote_url of the action microservice",
                    "status": "READY|STARTING|RETIRING"
                }
            }
        }
        Switching set format:
        [
            "ACTION_NAME": {
                "local": "START|STOP|STOP_WHEN_READY",
                "remote": "START|STARTING|STOP|STOP_WHEN_READY"
            }
        ]
        """
        self.state = {}
        self.change_set = {}

    def if_changing(self):
        return len(self.change_set) > 0

    def get_change_set(self):
        return self.change_set

    def local_action_loaded(self, name):
        self.state[name]["mode"] = "local"
        del self.change_set[name]["local"]

    def local_action_unloaded(self, name):
        del self.change_set[name]["local"]

    def remote_action_loaded(self, name):
        self.state[name]["mode"] = "remote"
        self.state[name]["remote"]["status"] = "READY"

    def remote_action_unloaded(self, name):
        del self.change_set[name]["remote"]

    def start_remote_action(self, name, url):
        if name not in self.state:
            self.state[name] = {}
        self.state[name]["remote"] = {"status": "STARTING", "url": url}

    def remote_action_started(self, name):
        self.change_set[name]["remote"] = "STARTING"

    def stop_remote_action(self, name):
        self.state[name]["remote"] = {}

    def get_remote_url(self, name):
        return self.state[name]["remote"]["url"]

    def get_state(self, name):
        return self.state.get(name, None)

    def set_change_set(self, name, mode):
        if name not in self.change_set:
            self.change_set[name] = {}
        if mode not in self.change_set[name]:
            self.change_set[name][mode] = "START"


class ActionOptimizerPolicy:
    """
    Template for action optimizer policy
    """

    def __init__(self) -> None:
        self.actions_state = None
        pass

    def set_actions_state(self, actions_state: ActionsState):
        self.actions_state = actions_state

    def check(self):
        pass


class DefaultPolicy(ActionOptimizerPolicy):
    """
    Default action optimizer policy, i.e. no automatic optimization
    """

    def check(self):
        if self.actions_state.get_state("use_enc") is None:
            self.actions_state.set_change_set("use_enc", "remote")


class ActionOptimizer:
    def __init__(
        self, kube: Kube, policy: ActionOptimizerPolicy = DefaultPolicy()
    ) -> None:
        self.kube = kube
        self.policy = policy
        self.actions_state = ActionsState()
        self.policy.set_actions_state(self.actions_state)
        pass

    def run(self):
        """
        The main optimization function.
        This gets invoked by JSROC regularly at a configured interval.
        """
        self.policy.check()
        if self.actions_state.if_changing():
            self.apply_actions_state()

    def apply_actions_state(self):
        """
        Apply any action configuration changes
        """
        # Update the actions depending on the change set
        change_set = self.actions_state.get_change_set()
        for name, changes in change_set.items():
            if "local" in changes:
                cmd = changes["local"]
                if cmd == "START":
                    self.load_action_module(name)
                    self.actions_state.local_action_loaded(name)
                elif cmd == "STOP":
                    self.unload_action_module(name)
                    self.actions_state.local_action_unloaded(name)
                elif cmd == "STOP_WHEN_READY":
                    # Check if remote action is ready
                    url = self.actions_state.get_remote_url(name)
                    if self.remote_action_ready_check(name, url):
                        self.unload_action_module(name)
                        self.actions_state.local_action_unloaded(name)

            if "remote" in changes:
                cmd = changes["remote"]
                if cmd == "START":
                    url = self.spawn_remote(name)
                    self.actions_state.start_remote_action(name, url)
                elif cmd == "STARTING":
                    url = self.actions_state.get_remote_url(name)
                    if self.remote_action_ready_check(name, url):
                        self.load_action_remote(url)
                        self.actions_state.remote_action_loaded(name)
                elif cmd == "STOP":
                    self.retire_remote(name)
                    # TODO: Need to check if it is safe to retire the pod
                    self.actions_state.stop_remote_action(name)
                elif cmd == "STOP_WHEN_READY":
                    # TODO: This is the same as STOP because we always deal with local changes first in this function
                    self.retire_remote(name)
                    self.actions_state.stop_remote_action(name)

    def kube_create(self, config):
        namespace = "default"  # TODO: hardcoded
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            # TODO: should we use jsorc's create function here
            try:
                logger.info(f"ActionOptimzer: creating {kind} for {name}")
                self.kube.create(kind, namespace, conf)
            except ApiException:
                logger.error(f"Error creating {kind} for {name}")

    def kube_delete(self, config):
        namespace = "default"  # TODO: hardcoded
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            # TODO: should we use jsorc's create function here
            try:
                logger.info(f"ActionOptimzer: deleting {kind} for {name}")
                # TODO: should we use jsorc's create function here
                self.kube.delete(kind, namespace, conf)
            except ApiException:
                logger.error(f"Error creating {kind} for {name}")

    def retire_remote(self, name):
        """
        Retire a microservice through the kube service
        """
        config = ACTION_CONFIGS[name]["remote"]
        self.kube_delete(config)

    def spawn_remote(self, name):
        """
        Spawn a microservice through the kube service
        """
        config = ACTION_CONFIGS[name]["remote"]
        self.kube_create(config)

    def load_action_remote(self, url):
        load_remote_actions(url)

    def load_action_module(self, name):
        """
        Load an action module
        """
        module = ACTION_CONFIGS[name]["module"]
        load_module_actions(module)

    def unload_action_remote(self, name):
        pass

    def unload_action_module(self, name):
        """
        Unload an action module
        """
        module = ACTION_CONFIGS[name]["module"]
        unload_module(module)

    def remote_action_ready_check(self, name, url):
        """
        Check if a remote action is ready by querying the action_spec endpoint
        """
        headers = {"content-type": "application/json"}
        res = requests.get(url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers)
        return res.status_code == 200
