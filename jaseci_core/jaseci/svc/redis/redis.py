from redis import Redis

from jaseci.svc import CommonService, ServiceState as Ss
from jaseci.utils.utils import logger
from .common import REDIS_CONFIG


#################################################
#                  REDIS HOOK                   #
#################################################


class RedisService(CommonService):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        super().__init__(RedisService)

        try:
            if self.is_ready():
                self.state = Ss.STARTED
                self.__redis(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    "Skipping Redis due to initialization failure!\n"
                    f"{e.__class__.__name__}: {e}"
                )
            self.app = None
            self.state = Ss.FAILED

    def __redis(self, hook):
        configs = self.get_config(hook)
        enabled = configs.pop("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.app = Redis(**configs, decode_responses=True)
            self.app.ping()
            self.state = Ss.RUNNING
        else:
            self.state = Ss.DISABLED

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

    def reset(self, hook):
        self.build(hook)

    def clear(self):
        if self.is_running():
            self.app.flushdb()

    ###################################################
    #                     CONFIG                      #
    ###################################################

    def get_config(self, hook) -> dict:
        return hook.build_config("REDIS_CONFIG", REDIS_CONFIG)


# ----------------------------------------------- #
