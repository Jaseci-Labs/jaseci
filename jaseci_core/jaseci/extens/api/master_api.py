"""
Master api as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.utils.id_list import IdList
import uuid


class MasterApi:
    """
    Master APIs for users creating and managing groups of sub users

    These APIs
    """

    def __init__(self, head_master):
        self.caller = None
        self.head_master_id = head_master
        self.sub_master_ids = IdList(self)

    @Interface.private_api(cli_args=["name"])
    def master_create(
        self,
        name: str,
        password: str = "",
        global_init: str = "",
        global_init_ctx: dict = {},
        other_fields: dict = {},
    ):
        """
        Create a master instance and return root node master object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        if self.sub_master_ids.has_obj_by_name(name):
            return {"response": f"{name} already exists", "success": False}
        ret = {}
        mast = self.user_creator(name, password, other_fields)
        ret["user"] = mast.serialize()
        if len(global_init):
            ret["global_init"] = self.user_global_init(
                mast, global_init, global_init_ctx
            )
        self.take_ownership(mast)
        ret["success"] = True
        return ret

    @Interface.private_api(cli_args=["name"])
    def master_get(self, name: str, mode: str = "default", detailed: bool = False):
        """
        Return the content of the master with mode
        Valid modes: {default, }
        """
        mas = self.sub_master_ids.get_obj_by_name(name)
        if not mas:
            return {"response": f"{name} not found"}
        else:
            return mas.serialize(detailed=detailed)

    @Interface.private_api()
    def master_list(self, detailed: bool = False):
        """
        Provide complete list of all master objects (list of root node objects)
        """
        masts = []
        for i in self.sub_master_ids.obj_list():
            masts.append(i.serialize(detailed=detailed))
        return masts

    @Interface.private_api(cli_args=["name"])
    def master_active_set(self, name: str):
        """
        Sets the default master master should use
        NOTE: Specail handler included in general_interface_to_api
        """
        mas = self.sub_master_ids.get_obj_by_name(name)
        if not mas:
            return {"response": f"{name} not found"}
        self.caller = mas.jid
        return {"response": f"You are now {mas.name}"}

    @Interface.private_api()
    def master_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self.caller = None
        return {"response": f"You are now {self.name}"}

    @Interface.private_api()
    def master_active_get(self, detailed: bool = False):
        """
        Returns the default master master is using
        """
        if self.caller:
            return self._h.get_obj(self._m_id, self.caller).serialize(detailed=detailed)
        else:
            return self.serialize(detailed=detailed)

    @Interface.private_api()
    def master_self(self, detailed: bool = False):
        """
        Returns the masters object
        """
        return self.serialize(detailed=detailed)

    @Interface.private_api(cli_args=["name"])
    def master_delete(self, name: str):
        """
        Permanently delete master with given id
        """
        if not self.sub_master_ids.has_obj_by_name(name):
            return {"response": f"{name} not found", "success": False}
        self.sub_master_ids.destroy_obj_by_name(name)
        self.user_destroyer(name)
        return {"response": f"{name} has been destroyed", "success": True}

    def take_ownership(self, m):
        """
        Assumes owenership over another master
        """
        m.head_master_id = self.jid
        m.give_access(self)
        m.save()
        self.sub_master_ids.add_obj(m)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sub_master_ids.obj_list():
            i.destroy()
