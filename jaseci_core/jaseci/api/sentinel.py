"""
Sentinel api functions as a mixin
"""
from jaseci.utils.id_list import id_list


class sentinel_api():
    """
    Sentinel APIs
    """

    def __init__(self):
        self.sentinel_ids = id_list(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list():
            i.destroy()
        super().destroy()
