"""
Super (master) api as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.prim.master import Master


class SuperApi:
    """Super APIs for creating nicknames for UUIDs and other long strings"""

    @Interface.admin_api(cli_args=["name"])
    def master_createsuper(
        self,
        name: str,
        password: str = "",
        global_init: str = "",
        global_init_ctx: dict = {},
        other_fields: dict = {},
    ):
        """
        Create a super instance and return root node super object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        if self.sub_master_ids.has_obj_by_name(name):
            return {"response": f"{name} already exists", "success": False}
        ret = {}
        mast = self.superuser_creator(name, password, other_fields)
        ret["user"] = mast.serialize()
        if len(global_init):
            ret["global_init"] = self.user_global_init(
                mast, global_init, global_init_ctx
            )
        self.take_ownership(mast)
        ret["success"] = True
        return ret

    @Interface.admin_api()
    def master_allusers(
        self, limit: int = 0, offset: int = 0, asc: bool = False, search: str = None
    ):
        """
        Returns info on a set of users, limit specifies the number of users to
        return and offset specfies where to start
        NOTE: Abstract interface to be overridden
        """

    @Interface.admin_api(cli_args=["mast"])
    def master_become(self, mast: Master):
        """
        Sets the default master master should use
        """
        self.caller = mast.jid
        self.save()
        return {"response": f"You are now {mast.name}"}

    @Interface.admin_api(cli_args=["mast"])
    def master_unbecome(self):
        """
        Unsets the default master master should use
        """
        self.caller = None
        return {"response": f"You are now {self.name}"}
