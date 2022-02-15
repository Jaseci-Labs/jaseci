"""
Master api as a mixin
"""
from jaseci.api.interface import interface
from jaseci.utils.id_list import id_list


class master_api():
    """Master APIs for creating nicknames for UUIDs and other long strings

    """

    def __init__(self, head_master):
        self._caller = self
        self.head_master_id = head_master
        self.sub_master_ids = id_list(self)

    @interface.private_api(cli_args=['name'])
    def master_create(self, name: str, set_active: bool = True,
                      other_fields: dict = {}):
        """
        Create a master instance and return root node master object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        from jaseci.element.master import master
        new_m = master(h=self._h, name=name)
        return self.make_me_head_master_or_destroy(new_m)

    @interface.private_api(cli_args=['name'])
    def master_get(self, name: str, mode: str = 'default',
                   detailed: bool = False):
        """
        Return the content of the master with mode
        Valid modes: {default, }
        """
        mas = self.sub_master_ids.get_obj_by_name(name)
        if(not mas):
            return {'response': f"{name} not found"}
        else:
            return mas.serialize(detailed=detailed)

    @interface.private_api()
    def master_list(self, detailed: bool = False):
        """
        Provide complete list of all master objects (list of root node objects)
        """
        masts = []
        for i in self.sub_master_ids.obj_list():
            masts.append(i.serialize(detailed=detailed))
        return masts

    @interface.private_api(cli_args=['name'])
    def master_active_set(self, name: str):
        """
        Sets the default master master should use
        NOTE: Specail handler included in general_interface_to_api
        """
        mas = self.sub_master_ids.get_obj_by_name(name)
        if(not mas):
            return {'response': f"{name} not found"}
        self._caller = mas
        return {'response': f'You are now {mas.name}'}

    @interface.private_api()
    def master_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self._caller = self
        return {'response': f'You are now {self.name}'}

    @interface.private_api()
    def master_active_get(self, detailed: bool = False):
        """
        Returns the default master master is using
        """
        return self._caller.serialize(detailed=detailed)

    @interface.private_api()
    def master_self(self, detailed: bool = False):
        """
        Returns the masters object
        """
        return self.serialize(detailed=detailed)

    @interface.private_api(cli_args=['name'])
    def master_delete(self, name: str):
        """
        Permanently delete master with given id
        """
        if(not self.sub_master_ids.has_obj_by_name(name)):
            return {'response': f"{name} not found"}
        self.sub_master_ids.destroy_obj_by_name(name)
        return {'response': f"{name} has been destroyed"}

    def make_me_head_master_or_destroy(self, m):
        """
        Utility to bring an object into sub masters
        """
        m.head_master_id = self.jid
        m.give_access(self)
        if(self.sub_master_ids.has_obj_by_name(m.name)):
            name = m.name
            m.destroy()
            return {'response': f"{name} already exists"}
        m.save()
        self.sub_master_ids.add_obj(m)
        return m.serialize()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sub_master_ids.obj_list():
            i.destroy()
