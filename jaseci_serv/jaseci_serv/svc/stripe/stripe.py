from jaseci.svc import StripeService as Ss
from .config import STRIPE_CONFIG

#################################################
#                  STRIPE APP                   #
#################################################


class StripeService(Ss):
    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("STRIPE_CONFIG", STRIPE_CONFIG)
