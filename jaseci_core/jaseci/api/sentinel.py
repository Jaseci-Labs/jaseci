"""
Sentinel api functions as a mixin
"""
from jaseci.utils.id_list import id_list
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import logger
import base64


class sentinel_api():
    """
    Sentinel APIs
    """

    def __init__(self):
        self.sentinel_ids = id_list(self)

    def api_sentinel_create(self, name: str):
        """
        Create blank sentinel and return object
        """
        snt = sentinel(h=self._h, name=name, code='# Jac Code')
        self.sentinel_ids.add_obj(snt)
        return snt.serialize()

    def api_sentinel_list(self, detailed: bool = False):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize(detailed=detailed))
        return snts

    def api_sentinel_delete(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """
        self.sentinel_ids.destroy_obj(snt)
        return [f'Sentinel {snt.id} successfully deleted']

    def api_sentinel_code_get(self, snt: sentinel):
        """
        Get sentinel implementation in form of Jac source code
        """
        return [snt.code]

    def api_sentinel_code_set(self, snt: sentinel, code: str, encoded: bool):
        """
        Set sentinel implementation with Jac source code
        """
        # TODO: HOTFIX for mobile jac file
        code = code.replace("take --> node;", "take -->;")
        if (encoded):
            try:
                code = base64.b64decode(code).decode()
                # TODO: HOTFIX for mobile jac file
                code = code.replace("take --> node;", "take -->;")
            except UnicodeDecodeError:
                logger.error(
                    f'Code encoding invalid for Sentinel {snt.id}!')
                return [f'Code encoding invalid for Sentinel {snt.id}!']
        # TODO: HOTFIX to force recompile jac code everytime
        if (snt.code == code and snt.is_active and False):
            return [f'Sentinel {snt.id} already registered and active!']
        else:
            snt.code = code
            snt.register_code()
            snt.save()
            if(snt.is_active):
                return [f'Sentinel {snt.id} registered and active!']
            else:
                return [f'Sentinel {snt.id} code issues encountered!']

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list():
            i.destroy()
        super().destroy()
