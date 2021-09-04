"""
Sentinel api functions as a mixin
"""
from jaseci.utils.id_list import id_list
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str
import uuid


class sentinel_api():
    """
    Sentinel APIs
    """

    def __init__(self):
        self.active_snt_id = None
        self.sentinel_ids = id_list(self)

    def api_sentinel_register(self, name: str, code: str = '',
                              encoded: bool = False, auto_run: str = 'init',
                              ctx: dict = {}, set_active: bool = True):
        """
        Create blank or code loaded sentinel and return object
        Auto_run is the walker to execute on register (assumes active graph
        is selected)
        """
        snt = self.sentinel_ids.get_obj_by_name(name, silent=True)
        new_gph = None
        if(not snt):
            snt = sentinel(m_id=self._m_id, h=self._h, name=name)
            self.sentinel_ids.add_obj(snt)
            new_gph = self.api_graph_create(set_active=True)
        if(code):
            if (encoded):
                code = b64decode_str(code)
            snt.register_code(code)
        if(snt.walker_ids.has_obj_by_name(auto_run) and self.active_gph_id):
            nd = self._h.get_obj(self._m_id, uuid.UUID(self.active_gph_id))
            self.api_walker_run(name=auto_run, nd=nd, ctx=ctx,
                                snt=snt)
        if(set_active):
            self.api_sentinel_active_set(snt)
        self.extract_snt_aliases(snt)
        if(new_gph):
            return [snt.serialize(), new_gph]
        return [snt.serialize()]

    def api_sentinel_pull(self, set_active: bool = True):
        """
        Copies global sentinel to local master
        """
        glob_id = self._h.get_glob('GLOB_SENTINEL')
        if(not glob_id):
            return ['No global sentinel is available!']
        g_snt = self._h.get_obj(self._m_id, uuid.UUID(glob_id)).duplicate()

        snt = self.sentinel_ids.get_obj_by_name(g_snt.name, silent=True)
        if(not snt):
            snt = sentinel(m_id=self._m_id, h=self._h, name=g_snt.name)
            self.sentinel_ids.add_obj(snt)
        if(set_active):
            self.api_sentinel_active_set(snt)
        return self.api_sentinel_set(code=g_snt.code_ir, snt=snt,
                                     mode='ir')

    def api_sentinel_get(self, snt: sentinel = None,
                         mode: str = 'default', detailed: bool = False):
        """
        Get a sentinel rendered with specific mode
        Valid modes: {default, code, ir, }
        """
        if(mode == 'code'):
            return snt._jac_ast.get_text()
        elif(mode == 'ir'):
            return snt.ir_dict()
        else:
            return snt.serialize(detailed=detailed)

    def api_sentinel_set(self, code: str, encoded: bool = False,
                         snt: sentinel = None, mode: str = 'default'):
        """
        Set code/ir for a sentinel, only replaces walkers/archs in sentinel
        Valid modes: {code, ir, }
        """
        if (encoded):
            code = b64decode_str(code)
        if(mode == 'code' or mode == 'default'):
            snt.register_code(code)
        elif(mode == 'ir'):
            snt.apply_ir(code)
            snt.run_start(snt._jac_ast)
            if(snt.runtime_errors):
                snt.is_active = False
        else:
            return [f'Invalid mode to set {snt}']
        if(snt.is_active):
            self.extract_snt_aliases(snt)
            return [f'{snt} registered and active!']
        else:
            return [f'{snt} code issues encountered!']

    def api_sentinel_list(self, detailed: bool = False):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize(detailed=detailed))
        return snts

    def api_sentinel_active_set(self, snt: sentinel):
        """
        Sets the default sentinel master should use
        """
        self.active_snt_id = snt.jid
        self.api_alias_register('active:sentinel', snt.jid)
        return [f'Sentinel {snt.id} set as default']

    def api_sentinel_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self.active_snt_id = None
        self.api_alias_delete('active:sentinel')
        return ['Default sentinel unset']

    def api_sentinel_active_global(self):
        """
        Sets the default master sentinel to the global sentinel
        Exclusive OR with pull strategy
        """
        glob_id = self._h.get_glob('GLOB_SENTINEL')
        if(not glob_id):
            return ['No global sentinel is available!']
        self.active_snt_id = glob_id
        self.api_alias_register('active:sentinel', glob_id)
        return [f'Global sentinel {glob_id} set as default']

    def api_sentinel_active_get(self, detailed: bool = False):
        """
        Returns the default sentinel master is using
        """
        if(self.active_snt_id):
            default = self._h.get_obj(
                self._m_id, uuid.UUID(self.active_snt_id))
            return default.serialize(detailed=detailed)
        else:
            return ['No default sentinel is selected!']

    def api_sentinel_delete(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """
        self.remove_snt_aliases(snt)
        if(self.active_snt_id == snt.jid):
            self.api_sentinel_active_unset()
        self.sentinel_ids.destroy_obj(snt)
        return [f'Sentinel {snt.id} successfully deleted']

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list():
            i.destroy()
        super().destroy()
