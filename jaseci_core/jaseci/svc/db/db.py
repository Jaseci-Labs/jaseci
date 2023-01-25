from jaseci.svc import CommonService
from .config import DB_CONFIG
from .manifest import DB_MANIFEST
from psycopg2 import connect as DBConnect

class DBService(CommonService):

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = DBConnect(**DB_CONFIG)
        self.app.autocommit = True


    ###################################################
    #                     COMMONS                     #
    ###################################################

    # def get(self, name):
    #     return self.app.get(name)

    # def set(self, name, val):
    #     self.app.set(name, val)

    # def exists(self, name):
    #     return self.app.exists(name)

    # def delete(self, name):
    #     self.app.delete(name)

    # def hget(self, name, key):
    #     return self.app.hget(name, key)

    # def hset(self, name, key, val):
    #     self.app.hset(name, key, val)

    # def hexists(self, name, key):
    #     return self.app.hexists(name, key)

    # def hdel(self, name, key):
    #     self.app.hdel(name, key)

    # def hkeys(self, name):
    #     return self.app.hkeys(name)

    ###################################################
    #                     CONFIG                      #
    ###################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("DB_CONFIG", DB_CONFIG)

    def build_manifest(self, hook) -> dict:
        return hook.service_glob("DB_MANIFEST", DB_MANIFEST)


