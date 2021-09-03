"""
Admin Global api functions as a mixin
"""
from jaseci.actor.sentinel import sentinel


class global_api():
    """
    Admin global APIs
    """

    def admin_api_global_set(self, name: str, value: str):
        """
        Set a config
        """
        ret = {'success': True}
        if(name == 'GLOB_SENTINEL' or name in self.valid_configs):
            ret['response'] = f"{name} is sacred!"
            ret['success'] = False
        else:
            self._h.save_glob(name, value)
            ret['response'] = f"Global variable '{name}' to '{value}' set!"
        return ret

    def admin_api_global_delete(self, name: str):
        """
        Delete a config
        """
        ret = {'success': True}
        if(name == 'GLOB_SENTINEL' or name in self.valid_configs):
            ret['response'] = f"{name} is sacred!"
            ret['success'] = False
        else:
            self._h.destroy_glob(name)
            ret['response'] = f"Global {name} deleted."
        return ret

    def admin_api_global_sentinel_set(self, snt: sentinel = None):
        """
        Set sentinel as globally accessible
        """
        for i in snt.get_deep_obj_list():
            i.make_read_only()
        self._h.save_glob('GLOB_SENTINEL', snt.jid)
        return {'response': f"Global sentinel set to '{snt}'!"}

    def admin_api_global_sentinel_unset(self):
        """
        Set sentinel as globally accessible
        """
        self._h.destroy_glob('GLOB_SENTINEL')
        return {'response': f"Global sentinel cleared!"}
