from redis import Redis

from jaseci.svc import CommonService
from .config import REDIS_CONFIG
from .kube import REDIS_KUBE


#################################################
#                  REDIS HOOK                   #
#################################################


class RedisService(CommonService):

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = Redis(**self.config, decode_responses=True)
        self.app.ping()

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def get(self, name):
        return self.app.get(name)

    def set(self, name, val):
        self.app.set(name, val)

    def exists(self, name):
        return self.app.exists(name)

    def delete(self, name):
        self.app.delete(name)

    def hget(self, name, key):
        return self.app.hget(name, key)

    def hset(self, name, key, val):
        self.app.hset(name, key, val)

    def hexists(self, name, key):
        return self.app.hexists(name, key)

    def hdel(self, name, key):
        self.app.hdel(name, key)

    def hkeys(self, name):
        return self.app.hkeys(name)

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def clear(self):
        if self.is_running():
            self.app.flushdb()

    ###################################################
    #                     CONFIG                      #
    ###################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("REDIS_CONFIG", REDIS_CONFIG)

    def build_kube(self, hook) -> dict:
        return hook.service_glob("REDIS_KUBE", REDIS_KUBE)


# ----------------------------------------------- #
