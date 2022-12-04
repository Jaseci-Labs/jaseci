from jaseci.svc import PrometheusService as Ps
from .config import PROMON_CONFIG


class PromotheusService(Ps):
    def build_config(self, hook) -> dict:
        return hook.service_glob("PROMON_CONFIG", PROMON_CONFIG)
