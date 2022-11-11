"""
Node api functions as a mixin
"""
from jaseci.api.interface import Interface
from jaseci.actor.sentinel import Sentinel


class NodeApi:
    """
    Node APIs

    The node set of APIs are used for execution and management of nodes.
    """

    def __init__(self):
        pass

    @Interface.private_api()
    def node_total(self, snt: Sentinel = None, detailed: bool = False):
        """
        Get total nodes known to sentinel
        """
        objects = snt.arch_ids.obj_list()
        node_objects = list(filter(lambda obj: obj.kind == "node", objects))
        return len(node_objects)

    @Interface.private_api()
    def node_list(self, snt: Sentinel = None, detailed: bool = False):
        """
        List nodes known to sentinel
        """
        nodes = []
        for i in snt.arch_ids.obj_list():
            if i.kind == "node":
                nodes.append(i.serialize(detailed=detailed))
        return nodes
