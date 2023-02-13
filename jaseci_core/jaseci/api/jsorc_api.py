"""
JSORC APIs
"""

import yaml
import json
from json import dumps, loads
from time import time
from base64 import b64decode

from jaseci import JsOrc
from jaseci.svc.kube_svc import KubeService
from jaseci.utils.actions.actions_manager import ActionManager

from jaseci.api.interface import Interface


class JsOrcApi:
    """
    API for managing JsOrc
    """

    @Interface.admin_api()
    def load_yaml(self, files: list, namespace: str = "default"):
        """
        applying list of yaml files without associating to any modules/services
        """

        try:
            kube = JsOrc.svc("kube").poke(KubeService)

            res = {}
            for file in files:
                for conf in yaml.safe_load_all(b64decode(file["base64"])):
                    kind = conf["kind"]
                    kube.create(kind, namespace, conf)
                    if not res.get(kind):
                        res[kind] = []
                    res[kind].append(conf)

            return res
        except Exception:
            return {"message": "load_yaml is not supported on non automated JsOrc!"}

    @Interface.admin_api(cli_args=["name"])
    def apply_yaml(self, name: str, file: list, unsafe_paraphrase: str = ""):
        """
        apply manifest yaml to specific service
        """

        new_config = {}

        config_version = str(time())

        for conf in yaml.safe_load_all(b64decode(file[0]["base64"])):
            kind = conf["kind"]
            labels = conf.get("metadata").get("labels")
            if not labels.get("config_version"):
                labels["config_version"] = config_version

            if not new_config.get(kind):
                new_config[kind] = []
            new_config[kind].append(conf)

        old_config = self._h.get_glob(name)
        if old_config:
            old_config = loads(old_config)
            old_config.pop("__OLD_CONFIG__", None)
            for kind, confs in old_config.items():
                names = []
                for conf in confs:
                    names.append(conf["metadata"]["name"])
                old_config[kind] = names

            new_config["__OLD_CONFIG__"] = old_config

            if unsafe_paraphrase == JsOrc.settings("UNSAFE_PARAPHRASE"):
                new_config["__UNSAFE_PARAPHRASE__"] = unsafe_paraphrase

        self._h.save_glob(name, dumps(new_config))

        return new_config

    @Interface.admin_api(cli_args=["name"])
    def service_refresh(self, name: str):
        """
        refreshing service's config. If JsOrc is not automated, service will restart else JsOrc will handle the rest
        """

        # will throw exception if not existing
        JsOrc.svc_reset(name)

        return {"success": True}

    @Interface.admin_api(cli_args=["name"])
    def service_call(self, svc: str, attrs: list = []):
        """
        temporary api for retreiving/calling attributes of specific instance.
        """

        svc = JsOrc.svc(svc)

        if not svc:
            return "Service (svc) field is required!"

        if not attrs:
            return "Attributes (attrs) field is required!"

        res = svc
        for at in attrs:
            attr = at.get("attr", False)
            if attr:
                res = getattr(res, attr)

            if callable:
                args = at.get("args", [])
                kwargs = at.get("kwargs", {})
                res = res(*args, **kwargs)

        try:
            # test if json serializable
            json.dumps(res)
            return res
        except Exception:
            return {"error": f"Not JSON Serializable! class {res.__class__.__name__}"}

    @Interface.admin_api(cli_args=["name"])
    def jsorc_actions_load(self, name: str, mode: str):
        """
        Load an action as remote or local mode through JSORC.
        JSORC will load the corresponding module or start a microservice if needed.
        Return the current status of the action.
        """
        action_manager = JsOrc.get("action_manager", ActionManager)
        action_manager.load_actions(name, mode)
        status = action_manager.get_actions_status(name)

        return {"success": True, "action_status": status}

    @Interface.admin_api(cli_args=["name"])
    def jsorc_actions_status(self, name: str):
        """
        Get the current status of an action
        """
        status = JsOrc.get("action_manager", ActionManager).get_actions_status(name)
        return {"success": True, "action_status": status}

    @Interface.admin_api(cli_args=["name"])
    def jsorc_actions_unload(
        self, name: str, mode: str = "auto", retire_svc: bool = True
    ):
        """
        Unload an action through JSORC.
        If retire_svc is set to True (true by default), it will also retire the corresponding microservice.
        """
        res = JsOrc.get("action_manager", ActionManager).unload_actions(
            name, mode, retire_svc
        )
        return {"success": res[0], "message": res[1]}

    @Interface.admin_api(cli_args=["config", "name"])
    def jsorc_actions_config(self, config: str, name: str):
        """
        Loading the config of an action module
        config: name of the ai kit package (e.g. jac_nlp.config, jac_vision.config)
        name: name of the action module (e.g. use_enc, bi_enc)
        """
        res = JsOrc.get("action_manager", ActionManager).load_action_config(
            config, name
        )
        return {"success": res}

    @Interface.admin_api()
    def jsorc_trackact_start(self):
        """ "
        Instruct JSORC to start tracking any changes in actions state
        """
        JsOrc.get("action_manager", ActionManager).actions_tracking_start()
        return {"success": True}

    @Interface.admin_api()
    def jsorc_trackact_stop(self):
        """ "
        Instruct JSORC to start tracking any changes in actions state
        """
        return JsOrc.get("action_manager", ActionManager).actions_tracking_stop()

    @Interface.admin_api()
    def jsorc_benchmark_start(self):
        """
        Tell JSORC to start collecting request performance metrics
        """
        JsOrc.get("action_manager", ActionManager).benchmark_start()
        return {"success": True}

    @Interface.admin_api()
    def jsorc_benchmark_report(self):
        """
        Report the collected request performance metrics of the currently ongoing benchmark
        """
        return JsOrc.get("action_manager", ActionManager).benchmark_report()

    @Interface.admin_api()
    def jsorc_benchmark_stop(self, report: bool = True):
        """
        End the benchmark period and report performance metrics
        """
        return JsOrc.get("action_manager", ActionManager).benchmark_stop(report)

    @Interface.admin_api()
    def jsorc_tracksys_start(self):
        """
        Ask JSORC to start tracking the state of the system as observed by JSORC on every interval.
        """
        JsOrc.get("action_manager", ActionManager).state_tracking_start()
        return {"success": True}

    @Interface.admin_api()
    def jsorc_tracksys_report(self):
        """
        Report the tracked system states so far
        """
        return JsOrc.get("action_manager", ActionManager).state_tracking_report()

    @Interface.admin_api()
    def jsorc_tracksys_stop(self):
        """
        Stop state tracking for JSORC
        """
        return JsOrc.get("action_manager", ActionManager).state_tracking_stop()

    @Interface.admin_api()
    def jsorc_actionpolicy_set(self, policy_name: str, policy_params: dict = {}):
        """
        Set an action optimization policy for JSORC
        """
        res = JsOrc.get("action_manager", ActionManager).set_action_policy(
            policy_name, policy_params
        )
        if res is True:
            return {
                "success": True,
                "message": f"Action optimization policy configured as {policy_name} with params {policy_params}",
            }
        else:
            return {"success": False, "message": res}

    @Interface.admin_api()
    def jsorc_actionpolicy_get(self):
        """
        Get the current active action optimization policy
        """
        policy = JsOrc.get("action_manager", ActionManager).get_action_policy()
        return {"success": True, "policy": policy}

    @Interface.admin_api()
    def jsorc_loadtest(self, test: str, experiment: str = "", mem: int = 0):
        """
        load test API. overwritten in jaseci_serv
        """
        pass
