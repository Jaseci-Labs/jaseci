from jaseci.svc import PromotheusService as Ps
from jaseci_serv.configs import PROMON_CONFIG
from jaseci_serv.kubes import PROMON_KUBE


class PromotheusService(Ps):
    def build_config(self, hook) -> dict:
        return hook.service_glob("PROMON_CONFIG", PROMON_CONFIG)

    def build_kube(self, hook) -> dict:
        return hook.service_glob("PROMON_KUBE", PROMON_KUBE)
