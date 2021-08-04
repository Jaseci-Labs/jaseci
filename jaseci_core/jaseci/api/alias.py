"""
Alias api as a mixin
"""


class alias_api():
    """
    APIs for Alias capability for savings alias for strings such as UUIDs
    """

    def __init__(self):
        self.alias_map = {}

    def api_alias_register(self, name: str, value: str):
        """
        Creates a string to string alias to be used by client
        """
        self.alias_map[name] = value
        return [f"Alias from '{name}' to '{value}' set!"]

    def api_alias_list(self):
        """
        List all string to string alias that client can use
        """
        return self.alias_map

    def api_alias_delete(self, name: str):
        """
        Remove string to string alias that client can use
        """
        if(name in self.alias_map.keys()):
            del self.alias_map[name]
            return [f'Alias {name} successfully deleted']
        else:
            return [f'Alias {name} not present']

    def api_alias_clear(self):
        """
        Remove all string to string alias that client can use
        """
        n = len(self.alias_map.keys())
        self.alias_map = {}
        return [f'All {n} aliases deleted']

    def extract_snt_aliases(self, snt):
        """
        Extract and register all aliases from sentinel
        """
        self.api_alias_register(f'sentinel:{snt.name}', snt.jid)
        for i in snt.walker_ids.obj_list():
            self.extract_wlk_aliases(snt, i)
        for i in snt.arch_ids.obj_list():
            self.extract_arch_aliases(snt, i)

    def extract_wlk_aliases(self, snt, wlk):
        """
        Extract and register all aliases from walker
        """
        self.api_alias_register(f'{snt.name}:walker:{wlk.name}', wlk.jid)

    def extract_arch_aliases(self, snt, arch):
        """
        Extract and register all aliases from architype
        """
        self.api_alias_register(f'{snt.name}:architype:{arch.name}', arch.jid)

    def remove_snt_aliases(self, snt):
        """
        Extract and register all aliases from sentinel
        """
        self.api_alias_delete(f'sentinel:{snt.name}')
        for i in snt.walker_ids.obj_list():
            self.remove_wlk_aliases(snt, i)
        for i in snt.arch_ids.obj_list():
            self.remove_arch_aliases(snt, i)

    def remove_wlk_aliases(self, snt, wlk):
        """
        Extract and register all aliases from walker
        """
        self.api_alias_delete(f'{snt.name}:walker:{wlk.name}')

    def remove_arch_aliases(self, snt, arch):
        """
        Extract and register all aliases from architype
        """
        self.api_alias_delete(f'{snt.name}:architype:{arch.name}')
