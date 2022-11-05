from jaseci.svc import JsOrcService as Js
from jaseci_serv.configs import JSORC_CONFIG


class JsOrcService(Js):
    def build_config(self, hook) -> dict:
        return hook.service_glob("JSORC_CONFIG", JSORC_CONFIG)
