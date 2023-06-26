"""
Admin Global api functions as a mixin
"""
from jaseci.utils.utils import manipulate_data
from jaseci.extens.api.interface import Interface
from jaseci.prim.sentinel import Sentinel
from json import dumps, loads


class GlobalApi:
    """
    Admin global APIs
    """

    @Interface.private_api(cli_args=["name"])
    def global_get(self, name: str):
        """
        Get a global
        """
        glob = self._h.get_glob(name)

        if isinstance(glob, (str, bytes, bytearray)):
            try:
                return loads(glob)
            except Exception:
                pass

        return glob

    @Interface.admin_api(cli_args=["name"])
    def global_set(self, name: str, value: str or dict or list or tuple):
        """
        Set a global
        """
        if name == "GLOB_SENTINEL":
            return f"{name} is sacred!"

        if not (value is None) and isinstance(value, (dict, list, tuple)):
            value = dumps(value)

        self._h.save_glob(name, value)
        return [f"Global '{name}' to '{value}' set!"]

    @Interface.admin_api(cli_args=["name"])
    def global_update(
        self,
        name: str,
        field_key: str or int or list or tuple,
        field_value: str
        or int
        or float
        or list
        or dict
        or bool
        or tuple
        or None,  # json serializable types
    ):
        """
        Update a key-value of a global
        """

        glob = self._h.get_glob(name)
        try:
            glob = manipulate_data(glob, field_key, field_value)
            self._h.save_glob(name, glob)
            return [
                f"Global '{name}' is updated with {field_key}:{field_value}. Current global value: {glob}"
            ]
        except Exception:
            return [
                f"Global {name} is not a dictionary or list. Uses global_set to set the value."
            ]

    @Interface.admin_api()
    def global_list(self):
        """
        Check a global is present
        """
        return self._h.list_glob()

    @Interface.admin_api(cli_args=["name"])
    def global_exists(self, name: str):
        """
        Check a global is present
        """
        return self._h.has_glob(name)

    @Interface.admin_api(cli_args=["name"])
    def global_delete(self, name: str):
        """
        Delete a global
        """
        if name == "GLOB_SENTINEL":
            return f"{name} is sacred!"

        self._h.destroy_glob(name)
        return [f"{name} Deleted."]

    @Interface.admin_api()
    def global_sentinel_set(self, snt: Sentinel = None):
        """
        Set sentinel as globally accessible
        """
        snt.make_read_only()
        snt.propagate_access()
        self._h.save_glob("GLOB_SENTINEL", snt.jid)
        return {"response": f"Global sentinel set to '{snt}'!"}

    @Interface.admin_api()
    def global_sentinel_unset(self):
        """
        Set sentinel as globally accessible
        """
        current = self.global_get("GLOB_SENTINEL")["value"]
        if current:
            snt = self._h.get_obj(self._m_id, current)
            for i in snt.get_deep_obj_list():
                i.make_private()
        self._h.destroy_glob("GLOB_SENTINEL")
        return {"response": "Global sentinel cleared!"}
