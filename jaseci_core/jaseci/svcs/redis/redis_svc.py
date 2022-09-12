"""
This module includes code related to hooking Jaseci's Redis to the
core engine.
"""
from jaseci.svcs import common_svc
from jaseci.utils.app_state import AppState as AS
from jaseci.utils.utils import logger
from redis import Redis

################################################
#                   DEFAULTS                   #
################################################

REDIS_CONFIG = {"enabled": True, "host": "localhost", "port": "6379", "db": "1"}

#################################################
#                  REDIS HOOK                   #
#################################################


class redis_svc(common_svc):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        super().__init__(redis_svc)

        try:
            if self.is_ready():
                self.state = AS.STARTED
                self.__redis(hook)
        except Exception as e:
            logger.error(
                "Skipping Redis due to initialization failure!\n"
                f"{e.__class__.__name__}: {e}"
            )
            self.app = None
            self.state = AS.FAILED

    def __redis(self, hook):
        configs = self.get_config(hook)
        enabled = configs.pop("enabled", True)

        if enabled:
            self.app = Redis(**configs, decode_responses=True)
            self.app.ping()
            self.state = AS.RUNNING
        else:
            self.state = AS.DISABLED

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
