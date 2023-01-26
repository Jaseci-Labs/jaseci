from redis import Redis

from jaseci.svc import CommonService
from .config import DATABASE_CONFIG as dbc
from .manifest import DATABASE_MANIFEST

import psycopg2


#################################################
#                  REDIS HOOK                   #
#################################################


class DatabaseService(CommonService):

    db_bypass = True

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = psycopg2.connect(
            host=dbc["host"],
            dbname=dbc["db"],
            user=dbc["user"],
            password=dbc["password"],
            port=dbc["port"],
        )

        self.manifest = DATABASE_MANIFEST


# ----------------------------------------------- #
