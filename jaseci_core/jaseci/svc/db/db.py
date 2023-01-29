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

    def cursor(self):
        self.app = DBConnect(**DB_CONFIG)
        return self.app.cursor()

    def close(self):
        return self.app.close()

    def commit(self):
        return self.app.commit()

    ###################################################
    #                     CONFIG                      #
    ###################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("DB_CONFIG", DB_CONFIG)

    def build_manifest(self, hook) -> dict:
        return hook.service_glob("DB_MANIFEST", DB_MANIFEST)


