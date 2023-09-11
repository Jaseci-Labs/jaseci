"""
Edge class for Jaseci

Each edge has an id, name, timestamp, the from node at the element of the edge
and the to node it is pointing to.
"""
from jaseci.prim.element import Element
from jaseci.prim.obj_mixins import Anchored
from jaseci.utils.utils import logger
import uuid
import sys


class Edge(Element, Anchored):
    """Edge class for Jaseci"""

    def __init__(self, **kwargs):
        self.from_node_id = None
        self.to_node_id = None
        self.bidirected: bool = False
        Anchored.__init__(self)
        Element.__init__(self, **kwargs)

    def from_node(self):
        """Returns node edge is pointing from"""
        ret = (
            self._h.get_obj(self._m_id, self.from_node_id)
            if self.from_node_id
            else None
        )
        if not ret:
            logger.critical(str(f"{self} disconnected from source node"))
            return None
        else:
            return ret

    def to_node(self):
        """Returns node edge is pointing to"""
        if not self.to_node_id:
            return None
        ret = self._h.get_obj(self._m_id, self.to_node_id) if self.to_node_id else None
        if not ret:
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
            node_set.remove(node_obj.jid)
            return self._h.get_obj(self._m_id, node_set[0])
        except ValueError:
            logger.critical(str(f"{self} disconnected to node {node_obj}"))
            return None

    def connect(self, source, target, bi_dir=False):
        """
        Connects both ends of the edge
        """
        self.from_node_id = source.jid
        self.to_node_id = target.jid
        source.smart_add_edge(self)
        target.smart_add_edge(self)
        self.set_bidirected(bi_dir)
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
        if not source and not target:
            return False
        if self.bidirected or ignore_direction:
            if source and source.jid not in [self.from_node_id, self.to_node_id]:
                return False
            if target and target.jid not in [self.from_node_id, self.to_node_id]:
                return False
        else:
            if source and source.jid != self.from_node_id:
                return False
            if target and target.jid != self.to_node_id:
                return False
        return True

    def is_fast(self):
        return sys.getsizeof(self.context) < 2000

    def save(self):
        """
        Write self through hook to persistent storage
        """

        if self.is_fast():
            self._persist = False
            if self.from_node_id:
                self.from_node().save()
            if self.to_node_id:
                self.to_node().save()
        super().save()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        base = self.from_node()
        target = self.to_node()
        base.smart_remove_edge(self) if base else None
        target.smart_remove_edge(self) if target else None
        super().destroy()

    def dot_str(self, node_map=None, edge_map=None, detailed=False):
        """
        DOT representation
        from_node -> to_node [context_key=contect_value]
        """

        def handle_str(str):
            return str[:32].replace('"', '\\"')

        from_name = (
            uuid.UUID(self.from_node().jid).hex
            if node_map is None
            else node_map.index(self.from_node().jid)
        )
        to_name = (
            uuid.UUID(self.to_node().jid).hex
            if node_map is None
            else node_map.index(self.to_node().jid)
        )
        dstr = f'"n{from_name}" -> "n{to_name}" [ '

        if detailed:
            dstr += f'id="{uuid.UUID(self.jid).hex}", '

        label = ""
        if edge_map:
            label = f"e{edge_map.index(self.jid)}"
        if self.name != "generic":
            label += f":{self.name}"

        dstr += f'label="{label}"'

        if self.bidirected:
            dstr += ', dir="both"'

        edge_dict = self.context
        for i in self.private_values():
            edge_dict.pop(i)

        if edge_dict and detailed:
            for k, v in edge_dict.items():
                if not isinstance(v, str) or v == "":
                    continue
                dstr += f', {k}="{handle_str(v)}"'

        dstr += " ]"

        return dstr + "\n"
