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
    unload_remote_actions,
    load_remote_actions,
    load_local_actions,
    live_actions,
    live_action_modules,
)
from jaseci.actions.remote_actions import remote_actions
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
                    self.actions_state.start_remote_service(name, url)
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
        """
        cur_state = self.actions_state.get_state(name)
        if cur_state is None:
            cur_state = self.actions_state.init_state(name)
            logger.info("init state")

        if cur_state["mode"] == "remote" and cur_state["remote"]["status"] == "READY":
            # Check if there is already a remote action loaded
            return

        url = self.actions_state.get_remote_url(name)
        if url is None:
            logger.info("spawning a uservice")
            # Spawn a remote microservice
            url = self.spawn_remote(name)
            self.actions_state.start_remote_service(name, url)
            cur_state = self.actions_state.get_state(name)

        if cur_state["remote"]["status"] == "STARTING":
            logger.info("service is starting")
            if_ready = self.remote_action_ready_check(name, url)
            if if_ready:
                self.actions_state.set_remote_action_ready(name)
                cur_state = self.actions_state.get_state(name)

        if cur_state["remote"]["status"] == "READY":
            logger.info("service is ready")
            load_remote_actions(url)
            self.actions_state.remote_action_loaded(name)

        logger.info(f"live_actions: {live_actions}")
        logger.info(f"live_action_modules: {live_action_modules}")
        logger.info(f"remote_actions: {remote_actions}")

    def load_action_local(self, name):
        """ """
        pass

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

        logger.info(f"live_actions: {live_actions}")
        logger.info(f"live_action_modules: {live_action_modules}")
        logger.info(f"remote_actions: {remote_actions}")

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
        self.actions_state.remote_action_unloaded(name)

        return (True, f"Remote actions from {url} unloaded.")

    def remote_action_ready_check(self, name, url):
        """
        Check if a remote action is ready by querying the action_spec endpoint
        TODO
        """
        if url is None:
            return False
        spec_url = url.rstrip("/") + ACTIONS_SPEC_LOC
        logger.info(f"Checking if remote action {name} is ready at {spec_url}")
        headers = {"content-type": "application/json"}
        try:
            res = requests.get(
                url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers, timeout=1
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            # Remote service not ready yet
            return False

        return res.status_code == 200
