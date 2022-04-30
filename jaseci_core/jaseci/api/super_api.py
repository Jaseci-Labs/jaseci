"""
Super (master) api as a mixin
"""
from jaseci.api.interface import interface
from jaseci.element.master import master


class super_api:
    """Super APIs for creating nicknames for UUIDs and other long strings"""

    @interface.admin_api(cli_args=["name"])
    def master_createsuper(
        self, name: str, set_active: bool = True, other_fields: dict = {}
    ):
        """
        Create a super instance and return root node super object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        from jaseci.element.super_master import super_master

        new_m = super_master(h=self._h, name=name)
        return self.make_me_head_master_or_destroy(new_m)

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
