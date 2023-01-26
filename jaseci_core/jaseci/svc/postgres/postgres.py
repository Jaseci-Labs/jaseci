from redis import Redis

from jaseci.svc import CommonService
from .config import POSTGRES_CONFIG as pgc
from .manifest import POSTGRES_MANIFEST

import psycopg2


#################################################
#                  REDIS HOOK                   #
#################################################


class PostgresService(CommonService):

    db_bypass = True

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = psycopg2.connect(
            host=pgc["host"],
            dbname=pgc["db"],
            user=pgc["user"],
            password=pgc["password"],
            port=pgc["port"],
        )

        self.manifest = POSTGRES_MANIFEST


# ----------------------------------------------- #
