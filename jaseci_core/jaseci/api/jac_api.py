"""
Jac tools api functions as a mixin
"""
from jaseci.api.interface import interface


class jac_api():
    """
    Jac tool APIs
    """

    @interface.cli_api
    def jac_build(self):
        pass

    @interface.cli_api
    def jac_test(self):
        pass

    @interface.cli_api
    def jac_run(self):
        pass
