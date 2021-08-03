"""
Architype api functions as a mixin
"""
from jaseci.actor.architype import architype
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel


class architype_api():
    """
    Architype APIs
    """

    def api_architype_create(self, code: str = '', encoded: bool = False):
        """
        Create blank or code loaded architype and return object
        """

    def api_architype_list(self, detailed: bool = False, snt: sentinel = None):
        """
        List architypes known to sentinel
        """

    def api_architype_delete(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """

    def api_architype_code_get(self, snt: sentinel = None):
        """
        Get sentinel implementation in form of Jac source code
        """
