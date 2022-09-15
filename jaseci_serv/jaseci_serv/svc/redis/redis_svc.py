from jaseci.svc import redis_svc as rs
from jaseci_serv.jaseci_serv.settings import REDIS_CONFIG


class redis_svc(rs):
    def get_config(self, hook) -> dict:
        return hook.build_config("REDIS_CONFIG", REDIS_CONFIG)
