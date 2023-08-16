"""
User API
"""
from jaseci.extens.api.interface import Interface
from jaseci.jsorc.jsorc import JsOrc


class UserApi:
    """
    User APIs for creating users (some functions should be override downstream)

    These User APIs enable the creation and management of users on a Jaseci machine.
    The creation of a user in this context is synonymous to the creation of a master
    Jaseci object. These APIs are particularly useful when running a Jaseci server
    or cluster in contrast to running JSCTL on the command line. Upon executing JSCTL
    a dummy admin user (super_master) is created and all state is dumped to a session
    file, though any users created during a JSCTL session will indeed be created as
    part of that session's state.
    """

    @Interface.public_api(cli_args=["name"])
    def user_create(
        self,
        name: str,
        password: str = "",
        global_init: str = "",
        global_init_ctx: dict = {},
        other_fields: dict = {},
        send_email: bool = True,
    ):
        """
        Create a new user (master object)

        This API is used to create users and optionally set them up with a graph and
        related initialization. In the context of
        JSCTL, any name is sufficient and no additional information is required.
        However, for Jaseci serving (whether it be the official Jaseci server, or a
        custom overloaded server) additional fields are required and should be added
        to the other_fields parameter as per the specifics of the encapsulating server
        requirements. In the case of the official Jaseci server, the name field must
        be a valid email, and a password field must be passed through other_fields.
        A number of other optional parameters can also be passed through other_feilds.
        \\vspace{3mm}\\par
        This single API call can also be used to fully set up and initialize a user
        by leveraging the global_init parameter. When set, this parameter attaches the
        user to the global sentinel, creates a new graph for the user, sets it as the
        active graph, then runs an initialization walker on the root node of this new
        graph. The initialization walker is identified by the name assigned to
        global_init. The default empty string assigned to global_init indicates this
        global setup should not be run.

        :param name: The user name to create. For Jaseci server this must be a valid
            email address.
        :param global_init: The name of an initialization walker. When set the user is
            linked to the global sentinel and the walker is run on a new active graph
            created for the user.
        :param global_init_ctx: Context to preload for the initialization walker
        :param other_fields: This parameter is used for additional fields required for
            overloaded interfaces. This parameter is not used in JSCTL, but is used
            by Jaseci server for the additional parameters of password, is_activated,
            and is_superuser.
        """
        ret = {}
        mast = self.user_creator(name, password, other_fields, send_email)
        if type(mast) is dict:  # in case of upstream error
            return mast
        ret["user"] = mast.serialize()
        self.seek_committer(mast)
        if len(global_init):
            ret["global_init"] = self.user_global_init(
                mast, global_init, global_init_ctx
            )
        ret["success"] = True
        return ret

    @Interface.admin_api(cli_args=["name"])
    def user_delete(self, name: str):
        """
        Delete new user (master object)

        This API is used to delete a user account.

        :param name: The user name to delete. For Jaseci server this must
        be a valid email address.

        """
        ret = {}
        ret["success"] = self.user_destroyer(name)
        if not ret["success"]:
            ret["status_code"] = 400
        return ret

    @Interface.private_api(cli_args=["name"])
    def user_deleteself(self):
        """
        Delete self (master object)

        This API is used to delete a user account.
        """
        ret = {}
        ret["success"] = self.user_destroyer(self.name)
        if not ret["success"]:
            ret["status_code"] = 400
        return ret

    def user_creator(
        self, name, password: str = "", other_fields: dict = {}, send_email=True
    ):
        """
        Abstraction for user creation for elegant overriding
        """

        return JsOrc.master(h=self._h, name=name)

    def superuser_creator(self, name, password: str = "", other_fields: dict = {}):
        """
        Abstraction for super user creation for elegant overriding
        """

        return JsOrc.super_master(h=self._h, name=name)

    def user_global_init(
        self,
        mast,
        global_init: str = "",
        global_init_ctx: dict = {},
    ):
        """
        Create a master instance and return root node master object

        other_fields used for additional fields for overloaded interfaces
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
