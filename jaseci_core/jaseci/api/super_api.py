"""
Super (master) api as a mixin
"""
from json import dumps
from jaseci.api.interface import interface
from jaseci.element.master import master


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
        if self.sub_master_ids.has_obj_by_name(name):
            return {"response": f"{name} already exists", "success": False}
        ret = {}
        mast = self.superuser_creator(name, other_fields)
        ret["user"] = mast.serialize()
        if len(global_init):
            ret["global_init"] = self.user_global_init(
                mast, global_init, global_init_ctx
            )
        self.take_ownership(mast)
        ret["success"] = True
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

    @interface.admin_api()
    def update_config(self, name: str, config: dict = {}, refresh: bool = True):
        """
        update global configs
        """

        hook = self._h

        if config:
            hook.save_glob(name, dumps(config))

        if refresh:
            if name == "TASK_CONFIG":
                hook.task_reset()
            elif name == "REDIS_CONFIG":
                hook.redis_reset()
