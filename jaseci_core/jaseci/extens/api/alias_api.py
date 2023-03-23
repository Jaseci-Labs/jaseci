"""
Alias api as a mixin
"""
from jaseci.extens.api.interface import Interface


class AliasAPI:
    """
    Alias APIs for creating nicknames for UUIDs and other long strings

    The alias set of APIs provide a set of `alias' management functions for
    creating and managing aliases for long strings such as UUIDs. If an alias'
    name is used as a parameter value in any API call, that parameter will see
    the alias' value instead. Given that references to all sentinels, walkers,
    nodes, etc. utilize UUIDs, it becomes quite useful to create pneumonic
    names for them. Also, when registering   sentinels, walkers, architype
    handy aliases are automatically generated. These generated aliases can
    then be managed using the alias APIs. Keep in mind that whenever an alias
    is created, all parameter values submitted to any API with the alias name
    will be replaced internally by its value. If you get in a bind, simply use
    the clear or delete alias APIs.
    """

    def __init__(self):
        self.alias_map = {}

    @Interface.private_api(cli_args=["name"])
    def alias_register(self, name: str, value: str):
        """Create string to string alias mapping that caller can use.

        Either create new alias string to string mappings or replace
        an existing mappings of a given alias name. Once registered the
        alias mapping is instantly active.

        Args:
            name (str): The name for the alias created by caller.
            value (str): The value for that name to map to (i.e., UUID)

        Returns:
            json: Fields include
                'response': Message of mapping that was created
        """
        self.alias_map[name] = value
        self.save()
        return {"response": f"Alias from '{name}' to '{value}' set!"}

    @Interface.private_api()
    def alias_list(self):
        """List all string to string alias that caller can use.

        Returns dictionary object of name to value mappings currently active.
        This API is quite useful to track not only the aliases the caller
        creates, but also the aliases automatically created as various Jaseci
        objects (walkers, architypes, sentinels, etc.) are created, changed,
        or destroyed.

        Returns:
            dictionary: Dictionary of active mappings
                'name': 'value'
                ...
        """
        return self.alias_map

    @Interface.private_api(cli_args=["name"])
    def alias_delete(self, name: str):
        """Delete an active string to string alias mapping.

        Removes a specific alias by its name. Only the alias is removed no
        actual objects are affected. Future uses of this name will not be
        mapped.

        Args:
            name (str): The name for the alias to be removed from caller.

        Returns:
            dictionary: Fields include
                'response': Message of success/failure to remove alias
                'success': True/False based on delete actually happening
        """
        if name in self.alias_map.keys():
            del self.alias_map[name]
            self.save()
            return {"response": f"Alias {name} successfully deleted", "success": True}
        else:
            return {"response": f"Alias {name} not present", "success": False}

    @Interface.private_api()
    def alias_clear(self):
        """Remove all string to string alias that client can use.

        Removes a all aliases. No actual objects are affected. Aliases will
        continue to be automatically generated when creating other Jaseci
        objects.

        Returns:
            dictionary: Fields include
                'response': Message of number of alias removed
                'removed': Number of aliases removed
        """
        n = len(self.alias_map.keys())
        self.alias_map = {}
        self.save()
        return {"response": f"All {n} aliases deleted", "removed": n}

    def extract_snt_aliases(self, snt):
        """
        Extract and register all aliases from sentinel
        """
        self.alias_register(f"sentinel:{snt.name}", snt.jid)
        for i in snt.arch_ids.obj_list():
            self.extract_arch_aliases(snt, i)
        self.save()

    def extract_arch_aliases(self, snt, arch):
        """
        Extract and register all aliases from architype
        """
        if arch.kind == "walker":
            self.alias_register(f"{snt.name}:walker:{arch.name}", arch.jid)
        else:
            self.alias_register(f"{snt.name}:architype:{arch.name}", arch.jid)

    def remove_snt_aliases(self, snt):
        """
        Extract and register all aliases from sentinel
        """
        self.alias_delete(f"sentinel:{snt.name}")
        for i in snt.arch_ids.obj_list():
            self.remove_arch_aliases(snt, i)
        self.save()

    def remove_arch_aliases(self, snt, arch):
        """
        Extract and register all aliases from architype
        """
        if arch.kind == "walker":
            self.alias_delete(f"{snt.name}:walker:{arch.name}")
        else:
            self.alias_delete(f"{snt.name}:architype:{arch.name}")
