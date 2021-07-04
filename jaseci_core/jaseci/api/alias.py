"""
Alias api as a mixin
"""


class alias_api():
    """
    APIs for Alias capability for savings alias for strings such as UUIDs
    """

    def __init__(self):
        self.alias_map = {}

    def api_alias_create(self, name: str, value: str):
        """
        Creates a string to string alias to be used by client
        """
        if(name in self.alias_map):
            return [f'Aliase {name} already created, please delete first']
        self.alias_map[name] = value
        return [f"Alias from '{name}' to '{value}' created!"]

    def api_alias_list(self):
        """
        List all string to string alias that client can use
        """
        return self.alias_map

    def api_alias_delete(self, name: str = None, all: bool = False):
        """
        Remove string to string alias that client can use
        """
        if(all):
            n = len(self.alias_map.keys())
            self.alias_map = {}
            return [f'All {n} aliases deleted']
        elif(name):
            if(name in self.alias_map.keys()):
                del self.alias_map[name]
                return [f'Alias {name} successfully deleted']
            else:
                return [f'Alias {name} not present']
        return ['Please enter alias to delete or specify all']
