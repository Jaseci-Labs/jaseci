"""
Graph  class for Jaseci

"""
from jaseci.graph.node import node
from jaseci.utils.id_list import id_list


class graph(node):
    """Graph class for Jaseci"""

    def __init__(self, *args, **kwargs):
        self.hd_node_ids = id_list(self)
        super().__init__(kind='root', *args, **kwargs)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.hd_node_ids.obj_list():
            i.destroy()
        super().destroy()

    def graph_dot_str(self):
        """
        DOT representation for graph.
        NOTE: This is different from the dot_str method for node intentionally
        because graph inherits node.
        """
        # node_list = self.get_network_nodes()
        edge_list = []  # self.get_network_paths()

        # Construct the graph string
        dstr = ''
        dstr += f'strict digraph {self.name} {{'
        # for n in node_list:
        #     dstr += f'    {n.dot_str()}'
        for e_list in edge_list:
            for e in e_list:
                dstr += f'    {e.dot_str()}'
        dstr += '}'
        return dstr
