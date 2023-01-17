import stripe
from jaseci.svc import CommonService
from .config import STRIPE_CONFIG

#################################################
#                  STRIPE APP                   #
#################################################


class StripeService(CommonService):

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = stripe
        if not self.config.get("api_key"):
            raise Exception("api_key is required!")
        self.app.api_key = self.config.get("api_key")

        if not self.config.get("webhook_key"):
            raise Exception("webhook_key is required!")
        self.webhook_key = self.config.get("webhook_key")

        self.fallback_walker = self.config.get("fallback_walker")
        if not self.fallback_walker:
            raise Exception("fallback_walker is required!")

        self.event_walker = self.config.get("event_walker", {})

    ####################################################
    #               COMMON GETTER/SETTER               #
    ####################################################

    def get_walker(self, event):
        return self.event_walker.get(event) or self.fallback_walker

    def get_event(self, request):
        return stripe.Webhook.construct_event(
            request["body"],
            request["headers"].get("HTTP_STRIPE_SIGNATURE"),
            self.webhook_key,
        )

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def reset(self, hook, start=True):
        stripe.api_key = None
        super().reset(hook, start)

    def build_config(self, hook) -> dict:
        return hook.service_glob("STRIPE_CONFIG", STRIPE_CONFIG)
