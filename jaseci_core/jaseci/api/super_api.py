"""
Super (master) api as a mixin
"""
from jaseci.api.interface import interface
from jaseci.element.master import master
import uuid


class super_api:
    """Super APIs for creating nicknames for UUIDs and other long strings"""

    @interface.admin_api(cli_args=["name"])
    def master_createsuper(
        self,
        name: str,
        global_init: str = "",
        global_init_ctx: dict = {},
        other_fields: dict = {},
    ):
        """
        Create a super instance and return root node super object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        from jaseci.element.super_master import super_master

        if self.sub_master_ids.has_obj_by_name(name):
            return {"response": f"{name} already exists", "success": False}
        ret = self.user_creator(
            super_master, name, global_init, global_init_ctx, other_fields
        )
        self.take_ownership(self._h.get_obj(self._m_id, uuid.UUID(ret["user"]["jid"])))
        return ret

    @interface.admin_api()
    def master_allusers(self, num: int = 0, start_idx: int = 0):
        """
        Returns info on a set of users, num specifies the number of users to
        return and start idx specfies where to start
        NOTE: Abstract interface to be overridden
        """

    @interface.admin_api(cli_args=["mast"])
    def master_become(self, mast: master):
        """
        Sets the default master master should use
        """
        self.caller = mast.jid
        return {"response": f"You are now {mast.name}"}

    @interface.admin_api(cli_args=["mast"])
    def master_unbecome(self):
        """
        Unsets the default master master should use
        """
        self.caller = None
        return {"response": f"You are now {self.name}"}
