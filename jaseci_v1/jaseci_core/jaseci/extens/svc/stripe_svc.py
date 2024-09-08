import stripe
from jaseci.jsorc.jsorc import JsOrc

#################################################
#                  STRIPE APP                   #
#################################################


@JsOrc.service("stripe", config="STRIPE_CONFIG")
class StripeService(JsOrc.CommonService):
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self):
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

    def get_event(self, body, headers):
        return stripe.Webhook.construct_event(
            body,
            headers.get("Stripe-Signature"),
            self.webhook_key,
        )

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def reset(self, hook, start=True):
        stripe.api_key = None
        super().reset(hook, start)
