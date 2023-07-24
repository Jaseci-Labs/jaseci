"""
Object api as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.prim.element import Element


class ObjectApi:
    """Object APIs for generalized operations on Jaseci objects

    ...
    """

    def __init__(self):
        self.perm_default = "private"
        self._valid_perms = ["public", "private", "read_only"]

    @Interface.private_api(cli_args=["name"])
    def global_get(self, name: str):
        """
        Get a global var
        """
        return {"value": self._h.get_glob(name)}

    @Interface.private_api(cli_args=["obj"])
    def object_get(self, obj: Element, depth: int = 0, detailed: bool = False):
        """Returns object details for any Jaseci object."""
        ret = obj.serialize(deep=depth, detailed=detailed)
        return ret

    @Interface.private_api(cli_args=["obj"])
    def object_set(
        self, obj: Element, ctx: dict, depth: int = 0, detailed: bool = False
    ):
        """Update a field in an object."""
        if "jid" in ctx:
            del ctx["jid"]
        for i in ctx.keys():
            if i in dir(obj) and not callable(getattr(obj, i)):
                setattr(obj, i, ctx[i])
        return obj.serialize(deep=depth, detailed=detailed)

    @Interface.private_api(cli_args=["obj"])
    def object_perms_get(self, obj: Element):
        """Returns object access mode for any Jaseci object."""
        return {"access": obj.j_access}

    @Interface.private_api(cli_args=["obj"])
    def object_perms_set(self, obj: Element, mode: str):
        """Sets object access mode for any Jaseci object."""
        ret = {}
        if mode not in self._valid_perms:
            ret["success"] = False
            ret["response"] = f"{mode} not valid, must be in {self._valid_perms}"
        else:
            getattr(obj, "make_" + mode)()
            ret["success"] = True
            ret["response"] = f"{obj} set to {mode}"
        return ret

    @Interface.private_api(cli_args=["mode"])
    def object_perms_default(self, mode: str):
        """Sets object access mode for any Jaseci object."""
        ret = {}
        if mode not in self._valid_perms:
            ret["success"] = False
            ret["response"] = f"{mode} not valid, must be in {self._valid_perms}"
        else:
            self.perm_default = mode
            ret["success"] = True
            ret["response"] = f"Default access for future objects set to {mode}"
        return ret

    @Interface.private_api(cli_args=["obj"])
    def object_perms_grant(self, obj: Element, mast: Element, read_only: bool = False):
        """Grants another user permissions to access a Jaseci object."""
        granted = obj.give_access(mast, read_only=read_only)
        ret = {"success": granted}
        if granted:
            ret["response"] = f"Access to {obj} granted to {mast}"
        else:
            ret["response"] = f"Cannot grant {mast} access to {obj}"
        return ret

    @Interface.private_api(cli_args=["obj"])
    def object_perms_revoke(self, obj: Element, mast: Element):
        """Remove permissions for user to access a Jaseci object."""
        revoked = obj.remove_access(mast)
        ret = {"success": revoked}
        if revoked:
            ret["response"] = f"Access to {obj} revoked from {mast}"
        else:
            ret["response"] = f"{mast} did not have access to {obj}"
        return ret

    @Interface.public_api()
    def info(self):
        """Provide information about this instance of Jaseci"""
        from jaseci import __version__, __creator__, __url__

        return {"Version": __version__, "Creator": __creator__, "URL": __url__}
