"""
Queue api functions as a mixin
"""
from base64 import b64decode
import json
from jaseci.svc.kubernetes import Kube
import yaml
from jaseci.api.interface import Interface


class JsOrcApi:
    """
    temporary
    """

    @Interface.admin_api(cli_args=["name"])
    def load_yaml(self, files: list, namespace: str = "default"):
        """
        temporary
        """

        kube = self._h.kube.app
        kube: Kube

        for file in files:
            for conf in yaml.safe_load_all(b64decode(file["base64"])):
                kube.call(namespace, conf)

    @Interface.admin_api(cli_args=["name"])
    def service_call(self, svc: str, attrs: list = []):
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
