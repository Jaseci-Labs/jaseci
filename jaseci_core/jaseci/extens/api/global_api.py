"""
Admin Global api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.prim.sentinel import Sentinel
import uuid


class GlobalApi:
    """
    Admin global APIs
    """

    @Interface.admin_api(cli_args=["name"])
    def global_set(self, name: str, value: str):
        """
        Set a global
        """
        ret = {"success": True}
        if name == "GLOB_SENTINEL" or name in self._valid_configs:
            ret["response"] = f"{name} is sacred!"
            ret["success"] = False
        else:
            self._h.save_glob(name, value)
            ret["response"] = f"Global variable '{name}' to '{value}' set!"
        return ret

    @Interface.admin_api(cli_args=["name"])
    def global_delete(self, name: str):
        """
        Delete a global
        """
        ret = {"success": True}
        if name == "GLOB_SENTINEL" or name in self._valid_configs:
            ret["response"] = f"{name} is sacred!"
            ret["success"] = False
        else:
            self._h.destroy_glob(name)
            ret["response"] = f"Global {name} deleted."
        return ret

    @Interface.admin_api()
    def global_sentinel_set(self, snt: Sentinel = None):
        """
        Make a sentinel globally accessible and set it as the global sentinel
        """
        snt.make_read_only()
        snt.propagate_access()
        self._h.save_glob("GLOB_SENTINEL", snt.jid)
        return {"response": f"Global sentinel set to '{snt}'!"}

    @Interface.admin_api()
    def global_sentinel_setaccess(self, snt: Sentinel = None):
        """
        Make a sentinel globally accessible
        """
        snt.make_read_only()
        snt.propagate_access()
        return {"response": f"Sentinel '{snt}' is now globally accessible (read-only)."}

    @Interface.admin_api()
    def global_sentinel_revokeaccess(self, snt: Sentinel = None):
        """
        Revoke the global accessibility of a sentinel. Making it private.
        """
        if snt.check_write_access(self._m_id):
            snt.make_private()
            snt.propagate_access()
            return {"response": f"Sentinel '{snt}' is now private."}
        else:
            return {"response:" "Insufficient permission."}

    @Interface.admin_api()
    def global_sentinel_unset(self):
        """
        Unset a global sentinel
        """
        current = self.global_get("GLOB_SENTINEL")["value"]
        if current:
            snt = self._h.get_obj(self._m_id, current)
            for i in snt.get_deep_obj_list():
                i.make_private()
        self._h.destroy_glob("GLOB_SENTINEL")
        return {"response": "Global sentinel cleared!"}
