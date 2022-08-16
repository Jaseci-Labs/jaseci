from datetime import datetime
from jaseci.api.interface import interface
import stripe

stripe_test_key = "sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"


class stripe_api:
    """
    Stripe APIs
    Set of APIs to expose jaseci stripe management
    """

    def __init__(self):
        stripe.api_key = self._h.resolve_glob("STRIPE_KEY", stripe_test_key)

    @interface.public_api()
    def stripe_webhook(data):
        """stripe webhooks"""
        # TODO: handle stripe webhooks
        try:
            return {"data": data}
        except Exception as e:
            return {"message": str(e)}
