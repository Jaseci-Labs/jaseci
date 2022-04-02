"""
Edge class for Jaseci

Each edge has an id, name, timestamp, the from node at the element of the edge
and the to node it is pointing to.
"""
from jaseci.element.element import element
from jaseci.element.obj_mixins import anchored
from jaseci.utils.utils import logger
import uuid


class edge(element, anchored):
    """Edge class for Jaseci"""

    def __init__(self, from_node=None, to_node=None, *args, **kwargs):
        self.from_node_id = None
        self.to_node_id = None
        self.bidirected: bool = False
        self.context = {}
        anchored.__init__(self)
        element.__init__(self, *args, **kwargs)
        if from_node:
            self.set_from_node(from_node)
        if to_node:
            self.set_to_node(to_node)

    def from_node(self):
        """Returns node edge is pointing from"""
        ret = self._h.get_obj(self._m_id, uuid.UUID(self.from_node_id)
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
        ret = self._h.get_obj(self._m_id, uuid.UUID(self.to_node_id)
                              ) if self.to_node_id else None
        if (not ret):
            logger.critical(str(f"{self} disconnected to target node"))
            return None
        else:
            return ret

    def nodes(self):
        """Returns both nodes connected to edge in a list"""
        return [self.to_node(), self.from_node()]

    def opposing_node(self, node_obj):
        """Returns opposite node edge is pointing from node_obj"""
        node_set = [self.to_node_id, self.from_node_id]
        try:
            node_set.remove(node_obj.id.urn)
            return self._h.get_obj(self._m_id, uuid.UUID(node_set[0]))
        except ValueError:
            logger.critical(
                str(f"{self} disconnected to node {node_obj}")
            )
            return None

    def set_from_node(self, node_obj):
        """
        Returns node edge is pointing from
        TODO: should check prior nodes edge_ids if is a reset
        """
        if self.to_node_id:
            if(not self.to_node().dimension_matches(node_obj,
                                                    silent=False)):
                return False
        self.from_node_id = node_obj.jid
        if(self.jid not in node_obj.edge_ids):
            node_obj.edge_ids.add_obj(self)
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
        self.to_node_id = node_obj.jid
        if(self.jid not in node_obj.edge_ids):
            node_obj.edge_ids.add_obj(self)
        self.save()
        return True

    def set_bidirected(self, bidirected: bool):
        """Sets/unsets edge to be bidirected"""
        self.bidirected = bidirected
        self.save()

    def is_bidirected(self):
        """Check if edge is bidirected"""
        return self.bidirected

    def connects(self, source=None, target=None, ignore_direction=False):
        """Test if a node or nodes are connected by edge"""
        if(not source and not target):
            return False
        if(self.bidirected or ignore_direction):
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

    def set_context(self, ctx, arch=None):
        """Assign values to context of edge"""
        if (arch is None):
            arch = self
        for i in ctx.keys():
            if (i not in arch.context.keys()):
                logger.warning(str(f"{i} not a context member of {self}"))
                continue
            else:
                self.context[i] = ctx[i]
        self.save()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        base = self.from_node()
        target = self.to_node()
        if base and self.jid in base.edge_ids:
            base.edge_ids.remove_obj(self)
        if target and self.jid in target.edge_ids:
            target.edge_ids.remove_obj(self)
        element.destroy(self)

    def dot_str(self, node_map=None, edge_map=None):
        """
        DOT representation
        from_node -> to_node [context_key=contect_value]
        """
        from_name = uuid.UUID(self.from_node(
        ).jid).hex if node_map is None else node_map.index(
            self.from_node().jid)
        to_name = uuid.UUID(self.to_node(
        ).jid).hex if node_map is None else node_map.index(
            self.to_node().jid)
        dstr = f'"n{from_name}" -> "n{to_name}" '

        dstr += f'[ id="{uuid.UUID(self.jid).hex}"'
        label = ''
        if(edge_map):
            label = f'e{edge_map.index(self.jid)}'
        if(self.name != 'generic'):
            label += f':{self.name}'
        if(label):
            dstr += f', label="{label}"'
        if(self.bidirected):
            dstr += f', dir="both"'

        edge_dict = self.context

        if (edge_dict):
            for k, v in edge_dict.items():
                if(not isinstance(v, str) or v == ""):
                    continue
                dstr += f', {k}="{v[:32]}"'

        dstr += ' ]'

        return dstr+'\n'
