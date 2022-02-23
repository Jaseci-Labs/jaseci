"""
Super (master) api as a mixin
"""
from jaseci.api.interface import interface


class super_api():
    """Super APIs for creating nicknames for UUIDs and other long strings

    """

    @interface.admin_api(cli_args=['name'])
    def master_createsuper(self, name: str, set_active: bool = True,
                           other_fields: dict = {}):
        """
        Create a super instance and return root node super object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        from jaseci.element.super_master import super_master
        new_m = super_master(h=self._h, name=name)
        return self.make_me_head_master_or_destroy(new_m)
