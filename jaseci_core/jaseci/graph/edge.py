"""
Edge class for Jaseci

Each edge has an id, name, timestamp, the from node at the element of the edge
and the to node it is pointing to.
"""
from jaseci.element import element
from jaseci.utils.obj_mixins import anchored
from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger
import uuid


class edge(element, anchored):
    """Edge class for Jaseci"""

    def __init__(self, from_node=None, to_node=None, *args, **kwargs):
        self.from_node_id = None
        self.to_node_id = None
        self.bidirected: bool = False
        self.context = {}
        self.activity_action_ids = id_list(self)
        anchored.__init__(self)
        element.__init__(self, *args, **kwargs)
        if from_node:
            self.set_from_node(from_node)
        if to_node:
            self.set_to_node(to_node)

    def from_node(self):
        """Returns node edge is pointing from"""
        ret = self._h.get_obj(uuid.UUID(self.from_node_id)
                              ) if self.from_node_id else None
        if (not ret):
            logger.critical(
                str(f"{self} disconnected from source node"))
            return None
        else:
            return ret

    def to_node(self):
        """Returns node edge is pointing to"""
        if (not self.to_node_id):
            return None
        ret = self._h.get_obj(uuid.UUID(self.to_node_id)
                              ) if self.to_node_id else None
        if (not ret):
            logger.critical(str(f"{self} disconnected to target node"))
            return None
        else:
            return ret

    def opposing_node(self, node_obj):
        """Returns node edge is pointing to"""
        node_set = [self.to_node_id, self.from_node_id]
        node_set.remove(node_obj.id.urn)
        ret = self._h.get_obj(uuid.UUID(node_set[0])) if len(
            node_set) == 1 and node_set[0] else None
        if (not ret):
            logger.critical(
                str(f"{self} disconnected to node {node_obj}")
            )
            return None
        else:
            return ret

    def set_from_node(self, node_obj):
        """
        Returns node edge is pointing from
        TODO: should check prior nodes edge_ids if is a reset
        """
        if self.to_node_id:
            if(not self.to_node().dimension_matches(node_obj,
                                                    silent=False)):
                return False
        self.from_node_id = node_obj.id.urn
        self.save()
        return True

    def set_to_node(self, node_obj):
        """
        Returns node edge is pointing to
        TODO: should check prior nodes edge_ids if is a reset
        """
        if self.from_node_id:
            if(not self.from_node().dimension_matches(node_obj,
                                                      silent=False)):
                return False
        self.to_node_id = node_obj.id.urn
        self.save()
        return True

    def set_bidirected(self, bidirected: bool):
        """Sets/unsets edge to be bidirected"""
        self.bidirected = bidirected

    def is_bidirected(self):
        """Check if edge is bidirected"""
        return self.bidirected

    def connects(self, source=None, target=None):
        """Test if a node or nodes are connected by edge"""
        if(not source and not target):
            return False
        if(self.bidirected):
            if(source and source.id.urn not in
               [self.from_node_id, self.to_node_id]):
                return False
            if(target and target.id.urn not in
               [self.from_node_id, self.to_node_id]):
                return False
        else:
            if(source and source.id.urn != self.from_node_id):
                return False
            if(target and target.id.urn != self.to_node_id):
                return False
        return True

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

    def dot_str(self):
        """
        DOT representation
        from_node -> to_node [context_key=contect_value]
        """
        from_name = uuid.UUID(self.from_node().jid).hex
        to_name = uuid.UUID(self.to_node().jid).hex
        arrow = '--' if self.bidirected else '->'
        dstr = f'{from_name} {arrow} {to_name} '

        edge_dict = self.context
        if (self.kind != 'generic'):
            edge_dict['_kind_'] = self.kind
        if (self.name != 'basic'):
            edge_dict['_name_'] = self.name

        if (edge_dict):
            dstr += '['
            num_items = 0
            for k, v in edge_dict.items():
                if(v is None or v == ""):
                    num_items += 1
                    continue
                if (num_items != 0):
                    dstr += ' '
                dstr += f'{k}={v}'

                num_items += 1
                if (num_items < len(edge_dict)):
                    dstr += ','
            dstr += ']'

        return dstr+'\n'
