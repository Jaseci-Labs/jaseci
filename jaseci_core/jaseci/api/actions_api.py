"""
Admin Global api functions as a mixin
"""
from jaseci.api.interface import interface


class actions_api():
    """
    Admin global APIs
    """

    @interface.admin_api()
    def actions_register(self, name: str, value: str):
        """
        """

    @interface.admin_api()
    def actions_get(self, name: str, value: str):
        """
        """

    @interface.admin_api()
    def actions_list(self, name: str, value: str):
        """
        """

    @interface.admin_api()
    def actions_delete(self, name: str, value: str):
        """
        """
