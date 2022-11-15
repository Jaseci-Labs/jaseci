"""
Edge api functions as a mixin
"""
from jaseci.api.interface import Interface
from jaseci.actor.sentinel import Sentinel


class EdgeApi:
    """
    Edge APIs

    The edge set of APIs are used for execution and management of edges.
    """

    def __init__(self):
        pass

    @Interface.private_api()
    def edge_total(self, snt: Sentinel = None, detailed: bool = False):
        """
        Get total edges known to sentinel
        """
        objects = snt.arch_ids.obj_list()
        edge_objects = list(filter(lambda obj: obj.kind == "edge", objects))
        return len(edge_objects)

    @Interface.private_api()
    def edge_list(self, snt: Sentinel = None, detailed: bool = False):
        """
        List edges known to sentinel
        """
        edges = []
        for i in snt.arch_ids.obj_list():
            if i.kind == "edge":
                edges.append(i.serialize(detailed=detailed))
        return edges
