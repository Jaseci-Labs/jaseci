"""
Queue api functions as a mixin
"""
import yaml
import json
from base64 import b64decode
from jaseci.svc.kubernetes import Kube
from jaseci.api.interface import Interface


class JsOrcApi:
    """
    temporary
    """

    @Interface.admin_api(cli_args=["name"])
    def jsorc_load_yaml(self, files: list, namespace: str = "default"):
        """
        temporary
        """

        kube = self._h.kube.app
        kube: Kube

        res = {}

        for file in files:
            for conf in yaml.safe_load_all(b64decode(file["base64"])):
                kind = conf["kind"]
                kube.create(kind, namespace, conf)
                if not res.get(kind):
                    res[kind] = []
                res[kind].append(conf)

        return res

    @Interface.admin_api(cli_args=["name"])
    def jsorc_service_call(self, svc: str, attrs: list = []):
        """
        temporary
        """

        from jaseci.svc import MetaService

        meta = self._h.meta
        meta: MetaService

        svc = meta.get_service(svc)

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
        JSORC will load the corresponding module or start a microservice if needed
        """
        hook = self._h
        if hook.meta.run_svcs:
            hook.jsorc.app.load_actions(name, mode)
            status = hook.jsorc.app.get_actions_status(name)
            return {"success": True, "action_status": status}
        else:
            return {"success": False, "message": "No running JSORC service."}

    @Interface.admin_api(cli_args=["name"])
    def jsorc_actions_status(self, name: str):
        """
        Get the current status of an action
        """
        hook = self._h
        if hook.meta.run_svcs:
            status = hook.jsorc.app.get_actions_status(name)
            return {"success": True, "action_status": status}
        else:
            return {"success": False, "message": "No running JSORC service."}

    @Interface.admin_api(cli_args=["name"])
    def jsorc_actions_unload(self, name: str, mode: str, retire_svc: bool = True):
        """
        Unload an action through JSORC.
        If retire_svc is set to True (true by default), it will also retire the corresponding microservice.
        """
        hook = self._h
        if hook.meta.run_svcs:
            hook.jsorc.app.unload_actions(name, mode)
        else:
            return {"success": False, "message": "No running JSORC service."}

    @Interface.admin_api()
    def jsorc_benchmark_start(self):
        """
        Tell JSORC to start collecting request performance metrics
        """
        pass

    @Interface.admin_api()
    def jsorc_benchmark_report(self):
        """
        Report the collected request performance metrics of the currently ongoing benchmark
        """
        pass

    @Interface.admin_api()
    def jsorc_benchmark_stop(self):
        """
        End the benchmark period and report performance metrics
        """
        pass
