from jaseci.svc import RedisService as Rs
from .config import REDIS_CONFIG


class RedisService(Rs):
    def build_config(self, hook) -> dict:
        return hook.service_glob("REDIS_CONFIG", REDIS_CONFIG)
