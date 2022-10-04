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

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.hd_node_ids.obj_list():
            i.destroy()
        super().destroy()
