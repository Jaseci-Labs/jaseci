"""
Admin Global api functions as a mixin
"""
from jaseci.actor.sentinel import sentinel
from .config import VALID_CONFIGS


class global_api():
    """
    Admin global APIs
    """

    def admin_api_global_get(self, name: str):
        """
        Get a global var
        """
        return self._h.get_glob(name)

    def admin_api_global_set(self, name: str, value: str):
        """
        Set a config
        """
        if(name == 'GLOB_SENTINEL' or name in VALID_CONFIGS):
            return [f"{name} is sacred!"]
        self._h.save_glob(name, value)
        return [f"Global variable '{name}' to '{value}' set!"]

    def admin_api_global_delete(self, name: str):
        """
        Delete a config
        """
        if(name == 'GLOB_SENTINEL' or name in VALID_CONFIGS):
            return [f"{name} is sacred!"]
        self._h.destroy_glob(name)
        return [f"Global {name} deleted."]

    def admin_api_global_sentinel_set(self, snt: sentinel = None):
        """
        Set sentinel as globally accessible
        """
        for i in snt.get_deep_obj_list():
            i.make_read_only()
        self._h.save_glob('GLOB_SENTINEL', snt.jid)
        return [f"Global sentinel set to '{snt}'!"]

    def admin_api_global_sentinel_unset(self):
        """
        Set sentinel as globally accessible
        """
        self._h.save_glob('GLOB_SENTINEL', None)
        return [f"Global sentinel cleared!"]
