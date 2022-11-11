from jaseci.svc.actions_optimizer.configs import ACTION_CONFIGS
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.utils.utils import logger
from jaseci.svc.kubernetes import Kube
from jaseci.svc.actions_optimizer.actions_state import ActionsState
from jaseci.svc.actions_optimizer.actions_optimizer_policy import (
    ActionsOptimizerPolicy,
    DefaultPolicy,
    BackAndForthPolicy,
)
from jaseci.actions.live_actions import (
    load_module_actions,
    unload_module,
    load_remote_actions,
)
import requests
import copy
from kubernetes.client.rest import ApiException


class ActionsOptimizer:
    def __init__(
        self, kube: Kube, policy: ActionsOptimizerPolicy = DefaultPolicy()
    ) -> None:
        self.kube = kube
        self.policy = policy
        self.actions_state = ActionsState()
        self.policy.set_actions_state(self.actions_state)

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
        for name, changes in copy.deepcopy(change_set).items():
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
                    self.actions_state.set_change_set(name, "remote", "STARTING")
                    if self.remote_action_ready_check(name, url):
                        self.load_action_remote(url)
                        self.actions_state.remote_action_loaded(name)
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
                logger.info(f"ActionsOptimzer: creating {kind} for {name}")
                self.kube.create(kind, namespace, conf)
            except ApiException:
                logger.error(f"Error creating {kind} for {name}")

    def kube_delete(self, config):
        namespace = "default"  # TODO: hardcoded
        for kind, conf in config.items():
            name = conf["metadata"]["name"]
            # TODO: should we use jsorc's create function here
            try:
                logger.info(
                    f"ActionsOptimzer: deleting {kind} for {name} for namespace {namespace}"
                )
                # TODO: should we use jsorc's create function here
                self.kube.delete(kind, name, namespace)
            except ApiException:
                logger.error(
                    f"Error creating {kind} for {name} for namespace {namespace}"
                )

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
        # TODO: Hack for testing

        url = "http://localhost:8001/"
        return url

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
        if url is None:
            return False
        logger.info(f"Checking if remote action {name} is ready at {url}")
        headers = {"content-type": "application/json"}
        res = requests.get(url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers)
        return res.status_code == 200
