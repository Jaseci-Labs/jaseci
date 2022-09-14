from jaseci.svc import RedisService as _RedisService
from jaseci_serv.jaseci_serv.settings import REDIS_CONFIG


class RedisService(_RedisService):
    def get_config(self, hook) -> dict:
        return hook.build_config("REDIS_CONFIG", REDIS_CONFIG)
