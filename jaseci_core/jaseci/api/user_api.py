"""
User API
"""
from jaseci.api.interface import interface


class user_api:
    """User APIs for creating users (some functions should be override downstream"""

    @interface.public_api(cli_args=["name"])
    def user_create(
        self,
        name: str,
        global_init: str = "",
        global_init_ctx: dict = {},
        other_fields: dict = {},
    ):
        """
        Create a master instance and return root node master object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        ret = {}
        mast = self.user_creator(name, other_fields)
        ret["user"] = mast.serialize()
        if len(global_init):
            ret["global_init"] = self.user_global_init(
                mast, global_init, global_init_ctx
            )
        ret["success"] = True
        return ret

    def user_creator(self, name, other_fields: dict = {}):
        """
        Abstraction for user creation for elegant overriding
        """
        from jaseci.element.master import master

        return master(h=self._h, name=name)

    def superuser_creator(self, name, other_fields: dict = {}):
        """
        Abstraction for super user creation for elegant overriding
        """
        from jaseci.element.super_master import super_master

        return super_master(h=self._h, name=name)

    def user_global_init(
        self,
        mast,
        global_init: str = "",
        global_init_ctx: dict = {},
    ):
        """
        Create a master instance and return root node master object

        other_fields used for additional feilds for overloaded interfaces
        (i.e., Dango interface)
        """
        return mast.sentinel_active_global(
            auto_run=global_init,
            auto_run_ctx=global_init_ctx,
            auto_create_graph=True,
        )

    def user_destroyer(self, name: str):
        """
        Permanently delete master with given id
        """
        pass
