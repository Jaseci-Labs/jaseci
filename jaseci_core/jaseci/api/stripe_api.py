"""
Super (master) api as a mixin
"""
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

    @interface.admin_api()
    def get_config(self, name: str):
        """get stripe config by name"""

    @interface.admin_api()
    def set_config(self, name: str, value: str):
        """set stripe config"""

    @interface.admin_api()
    def stripe_init(self):
        """initialize stripe"""
