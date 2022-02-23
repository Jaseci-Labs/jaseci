"""
Admin Global api functions as a mixin
"""
from jaseci.api.interface import interface
from jaseci.actor.sentinel import sentinel
import uuid


class global_api():
    """
    Admin global APIs
    """

    @interface.admin_api(cli_args=['name'])
    def global_set(self, name: str, value: str):
        """
        Set a global
        """
        ret = {'success': True}
        if(name == 'GLOB_SENTINEL' or name in self._valid_configs):
            ret['response'] = f"{name} is sacred!"
            ret['success'] = False
        else:
            self._h.save_glob(name, value)
            ret['response'] = f"Global variable '{name}' to '{value}' set!"
        return ret

    @interface.admin_api(cli_args=['name'])
    def global_delete(self, name: str):
        """
        Delete a global
        """
        ret = {'success': True}
        if(name == 'GLOB_SENTINEL' or name in self._valid_configs):
            ret['response'] = f"{name} is sacred!"
            ret['success'] = False
        else:
            self._h.destroy_glob(name)
            ret['response'] = f"Global {name} deleted."
        return ret

    @interface.admin_api()
    def global_sentinel_set(self, snt: sentinel = None):
        """
        Set sentinel as globally accessible
        """
        for i in snt.get_deep_obj_list():
            i.make_read_only()
        self._h.save_glob('GLOB_SENTINEL', snt.jid)
        return {'response': f"Global sentinel set to '{snt}'!"}

    @interface.admin_api()
    def global_sentinel_unset(self):
        """
        Set sentinel as globally accessible
        """
        current = self.global_get('GLOB_SENTINEL')['value']
        if(current):
            snt = self._h.get_obj(self._m_id, uuid.UUID(current))
            for i in snt.get_deep_obj_list():
                i.make_private()
        self._h.destroy_glob('GLOB_SENTINEL')
        return {'response': f"Global sentinel cleared!"}
