"""
Graph  class for Jaseci

"""
from core.graph.node import node
from core.utils.id_list import id_list


class graph(node):
    """Node class for Jaseci"""

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
