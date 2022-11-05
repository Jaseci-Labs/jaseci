from jaseci.svc import RedisService as Rs
from jaseci_serv.configs import REDIS_CONFIG
from jaseci_serv.kubes import REDIS_KUBE


class RedisService(Rs):
    def build_config(self, hook) -> dict:
        return hook.service_glob("REDIS_CONFIG", REDIS_CONFIG)

    def build_kube(self, hook) -> dict:
        return hook.service_glob("REDIS_KUBE", REDIS_KUBE)
