"""
Graph api functions as a mixin
"""
from jaseci.utils.id_list import id_list


class graph_api():
    """
    Graph APIs
    """

    def __init__(self):
        self.graph_ids = id_list(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.graph_ids.obj_list():
            i.destroy()
        super().destroy()
