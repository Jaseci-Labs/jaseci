from jaseci.svc import RedisService as rs
from jaseci_serv.jaseci_serv.settings import REDIS_CONFIG


class RedisService(rs):
    def get_config(self, hook) -> dict:
        return hook.build_config("REDIS_CONFIG", REDIS_CONFIG)
