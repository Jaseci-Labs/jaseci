"""
Graph  class for Jaseci

"""
from jaseci.graph.node import node
from jaseci.utils.id_list import id_list


class graph(node):
    """Graph class for Jaseci"""

    def __init__(self, *args, **kwargs):
        self.hd_node_ids = id_list(self)
        node.__init__(self, name='root', kind='node', *args, **kwargs)

    def get_all_nodes(self, node_list=None):
        """
        Returns all reachable nodes
        node_list is used internally for recursion
        """
        if(not isinstance(node_list, list)):
            node_list = []

        # if cycle detected in path
        if(self in node_list):
            return node_list

        node_list.append(self)

        for i in self.attached_nodes():
            graph.get_all_nodes(i, node_list)

        return node_list

    def get_all_edges(self):
        """
        Returns all reachable edges
        """
        edge_set = set()
        node_list = self.get_all_nodes()

        for i in node_list:
            for e in i.attached_edges():
                edge_set.add(e)

        return list(edge_set)

    def graph_dot_str(self):
        """
        DOT representation for graph.
        NOTE: This is different from the dot_str method for node intentionally
        because graph inherits node.
        """
        node_list = self.get_all_nodes()
        edge_list = self.get_all_edges()
        node_map = [i.jid for i in node_list]
        edge_map = [i.jid for i in edge_list]

        # Construct the graph string
        dstr = ''
        dstr += f'strict digraph {self.name} {{\n'
        for n in node_list:
            dstr += f'    {n.dot_str(node_map)}'
        for e in edge_list:
            dstr += f'    {e.dot_str(node_map, edge_map)}'
        dstr += '}'
        return dstr

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.hd_node_ids.obj_list():
            i.destroy()
        super().destroy()
