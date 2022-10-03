"""
Graph  class for Jaseci

"""
from collections import OrderedDict
from jaseci.graph.node import Node
from jaseci.utils.id_list import IdList


class Graph(Node):
    """Graph class for Jaseci"""

    def __init__(self, **kwargs):
        self.hd_node_ids = IdList(self)
        Node.__init__(self, **kwargs)
        self.name = "root"
        self.kind = "node"

        # Node.__init__(self, name="root", kind="node", **kwargs)

    def get_all_nodes(self, depth: int = 0):
        """
        Returns all reachable nodes
        """

        childs = {self.jid: self}
        nodes = OrderedDict(childs)
        depth -= 1

        while len(childs) and depth != 0:
            new_childs = OrderedDict()
            for child in childs.values():
                for _ch in child.attached_nodes():
                    if not (_ch.jid in nodes):
                        new_childs.update({_ch.jid: _ch})

            childs = new_childs
            nodes.update(childs)
            depth -= 1

        return nodes.values()

    def get_all_edges(self, nodes: list = None, depth: int = 0):
        """
        Returns all reachable edges
        """
        edges = OrderedDict()
        node_list = self.get_all_nodes(depth=depth) if nodes is None else nodes

        for nd in node_list:
            for _ch in nd.attached_edges():
                if not (_ch.jid in edges) and _ch.to_node() in node_list:
                    edges.update({_ch.jid: _ch})

        return edges.values()

    def graph_dot_str(self, detailed=False, depth: int = 0):
        """
        DOT representation for graph.
        NOTE: This is different from the dot_str method for node intentionally
        because graph inherits node.
        """
        node_list = self.get_all_nodes(depth=depth)
        edge_list = self.get_all_edges(nodes=node_list)
        node_map = [i.jid for i in node_list]
        edge_map = [i.jid for i in edge_list]

        # Construct the graph string
        dstr = ""
        dstr += f"strict digraph {self.name} {{\n"
        for n in node_list:
            dstr += f"    {n.dot_str(node_map, detailed)}"
        for e in edge_list:
            dstr += f"    {e.dot_str(node_map, edge_map, detailed)}"
        dstr += "}"
        return dstr

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.hd_node_ids.obj_list():
            i.destroy()
        super().destroy()
