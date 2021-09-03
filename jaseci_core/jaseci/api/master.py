"""
Master api as a mixin
"""

from jaseci.utils.id_list import id_list


class master_api():
    """Master APIs for creating nicknames for UUIDs and other long strings

    """

    def __init__(self):
        self.head_master_id = None
        self.sub_master_ids = id_list(self)

    def api_master_create(self, name: str, set_active: bool = True):
        """
        Create a master instance and return root node master object
        """
        mas = type(self)(h=self._h, name=name)
        self.sub_master_ids.add_obj(mas)
        return mas.serialize()

    def api_master_get(self, name: str, mode: str = 'default',
                       detailed: bool = False):
        """
        Return the content of the master with mode
        Valid modes: {default, dot, }
        """

    def api_master_list(self, detailed: bool = False):
        """
        Provide complete list of all master objects (list of root node objects)
        """

    def api_master_active_set(self, name: str):
        """
        Sets the default master master should use
        """

    def api_master_active_unset(self):
        """
        Unsets the default sentinel master should use
        """

    def api_master_active_get(self, detailed: bool = False):
        """
        Returns the default master master is using
        """

    def api_master_delete(self, name: str):
        """
        Permanently delete master with given id
        """

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sub_master_ids.obj_list():
            i.destroy()
        super().destroy()
