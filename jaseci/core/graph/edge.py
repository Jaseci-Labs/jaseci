"""
Edge class for Jaseci

Each edge has an id, name, timestamp, the from node at the element of the edge
and the to node it is pointing to.
"""
from core.element import element
from core.element import anchored
from core.utils.id_list import id_list
from core.utils.utils import logger
import uuid


class edge(element, anchored):
    """Edge class for Jaseci"""

    def __init__(self, from_node=None, to_node=None, *args, **kwargs):
        self.from_node_id = None
        self.to_node_id = None
        self.context = {}
        self.activity_action_ids = id_list(self)
        super().__init__(*args, **kwargs)
        if from_node:
            self.set_from_node(from_node)
        if to_node:
            self.set_to_node(to_node)

    def from_node(self):
        """Returns node edge is pointing from"""
        if (not self.from_node_id):
            return None
        ret = self._h.get_obj(uuid.UUID(self.from_node_id))
        if (not ret):
            logger.error(
                str("{} disconnected from node".format(self))
            )
            element.destroy(self)
        else:
            return ret

    def to_node(self):
        """Returns node edge is pointing to"""
        if (not self.to_node_id):
            return None
        ret = self._h.get_obj(uuid.UUID(self.to_node_id))
        if (not ret):
            logger.error(
                str("{} disconnected to node".format(self))
            )
            element.destroy(self)
        else:
            return ret

    def set_from_node(self, node_obj):
        """Returns node edge is pointing from"""
        if self.to_node_id:
            if(not self.to_node().dimension_matches(node_obj,
                                                    silent=False)):
                return
        self.from_node_id = node_obj.id.urn
        self.save()

    def set_to_node(self, node_obj):
        """Returns node edge is pointing to"""
        if self.from_node_id:
            if(not self.from_node().dimension_matches(node_obj,
                                                      silent=False)):
                return
        self.to_node_id = node_obj.id.urn
        self.save()

    def switch_direction(self):
        """
        Switches direction of edge, does not allow if such an edge
        already exists
        """

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.activity_action_ids.obj_list():
            i.destroy()
        base = self.from_node()
        target = self.to_node()
        if base and self in base.edge_ids.obj_list():
            base.edge_ids.remove_obj(self)
        if target and self in target.edge_ids.obj_list():
            target.edge_ids.remove_obj(self)
        element.destroy(self)
