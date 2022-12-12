"""
Module that manage and optimizes the actions configuration of Jaseci
"""

from jaseci.svc.actions_optimizer.configs import ACTION_CONFIGS
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.utils.utils import logger
from jaseci.svc import Kube
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
import copy
from kubernetes.client.rest import ApiException


class ActionsOptimizer:
    def __init__(
        self,
        kube=None,
        namespace: str = "default",
    ) -> None:
        self.kube = kube
        self.actions_state = ActionsState()
        self.actions_change = {}
        self.jsorc_interval = 0
        self.namespace = namespace

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
            return {"mode": self.actions_state.get_state(name)["mode"]}

    def retire_remote(self, name):
        """
        Retire a microservice through the kube service
        """
        config = ACTION_CONFIGS[name]["remote"]
        self.kube_delete(config)
        self.actions_state.remove_remote(name)

    def spawn_remote(self, name):
        """
        Spawn a microservice through the kube service
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
        pass

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

        loaded_mod = load_module_actions(module, cur_state["module"]["loaded_module"])
        self.action_prep(name)
        self.actions_state.module_action_loaded(name, module, loaded_mod)
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
        loaded_module = cur_state["module"]["loaded_module"]

        unload_module(module_name)
        unload_module(loaded_module)
        # logger.info("deleting loaded module")
        # logger.info(loaded_module)
        # del loaded_module

        # Alright we are in prime hack terrotoriy now lol
        # core_mod_name = module_name.split(".")[-1]
        # if core_mod_name == "bi_enc":
        #     possible_module_name = [
        #         module_name,
        #         "jaseci_ai_kit.modules.encoders",
        #         "jaseci_ai_kit.modules.encoders.bi_enc",
        #     ]
        # else:
        #     possible_module_name = [
        #         module_name,
        #         f"jaseci_ai_kit.modules.{core_mod_name}",
        #         f"jaseci_ai_kit.modules.{core_mod_name}.{core_mod_name}",
        #     ]
        # for mod in possible_module_name:
        #     unload_module(mod)

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
