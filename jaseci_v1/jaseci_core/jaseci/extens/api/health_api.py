"""
Health APIs
"""

from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.api.interface import Interface


class HealthApi:
    """
    API for readiness probe
    """

    @Interface.public_api(allowed_methods=["get"])
    def health(self):
        """
        readiness probe
        """
        # to update
        # we might need to return some other information here
        return JsOrc.__running__
