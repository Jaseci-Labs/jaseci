from jaseci.svc import ElasticService as Es
from .config import ELASTIC_CONFIG


#################################################
#                  ELASTIC APP                  #
#################################################


class ElasticService(Es):

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("ELASTIC_CONFIG", ELASTIC_CONFIG)
