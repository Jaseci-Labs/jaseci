from .id_list import id_list
from .utils import logger

import json


def json_str_to_jsci_dict(input_str, parent_obj=None):
    """
    Helper function to convert JSON strings to dictionarys with _ids list
    conversions from hex to UUID

    ret_obj is the owning object for id_list objects
    """
    try:
        obj_fields = json.loads(input_str)
    except ValueError:
        logger.error(
            str(f'Invalid jsci_obj string {input_str} on {parent_obj.id.urn}'))
        obj_fields = {}
    for i in obj_fields.keys():
        if(str(i).endswith("_ids") and isinstance(obj_fields[i], list)):
            obj_fields[i] = id_list(
                parent_obj=parent_obj, in_list=obj_fields[i])
    return obj_fields


class mem_hook():
    """
    Set of virtual functions to be used as hooks to allow access to
    the complete set of items across jaseci object types. This class contains
    a number of blank function calls to be bound extrenally and passed
    to the objects. They return jaseci core types.
    """

    def __init__(self):
        from jaseci.actions.live_actions import get_global_actions
        self.mem = {'global': {}}
        self.global_action_list = get_global_actions(self)

    def get_obj(self, caller_id, item_id, override=False):
        """
        Get item from session cache by id, then try store
        TODO: May need to make this an object copy so you cant do mem writes
        """
        if(item_id in self.mem.keys()):
            ret = self.mem[item_id]
            if(override or ret.check_read_access(caller_id)):
                return ret
        else:
            ret = self.get_obj_from_store(item_id)
            self.mem[item_id] = ret
            if(override or (ret is not None and
               ret.check_read_access(caller_id))):
                return ret

    def has_obj(self, item_id):
        """
        Checks for object existance
        """
        if(item_id in self.mem.keys()):
            return True
        else:
            return self.has_obj_in_store(item_id)

    def save_obj(self, caller_id, item, persist=False):
        """Save item to session cache, then to store"""
        if(item.check_write_access(caller_id)):
            self.mem[item.id] = item
            if (persist):
                self.save_obj_to_store(item)

    def destroy_obj(self, caller_id, item, persist=False):
        """Destroy item from session cache then  store"""
        if(item.check_write_access(caller_id)):
            self.mem[item.id] = None
            del self.mem[item.id]
            if(persist):
                self.destroy_obj_from_store(item)

    def get_glob(self, name):
        """
        Get global config from session cache by id, then try store
        """
        if(name in self.mem['global'].keys()):
            return self.mem['global'][name]
        else:
            ret = self.get_glob_from_store(name)
            self.mem['global'][name] = ret
            return ret

    def has_glob(self, name):
        """
        Checks for global config existance
        """
        if(name in self.mem['global'].keys()):
            return True
        else:
            return self.has_glob_in_store(name)

    def resolve_glob(self, name, default=None):
        """
        Util function for returning config if exists otherwise default
        """
        if(self.has_glob(name)):
            return self.get_glob(name)
        else:
            return default

    def save_glob(self, name, value, persist=True):
        """Save global config to session cache, then to store"""
        self.mem['global'][name] = value
        if (persist):
            self.save_glob_to_store(name, value)

    def list_glob(self):
        """Lists all configs present"""
        glob_list = self.list_glob_from_store()
        if(glob_list):
            return glob_list
        else:
            return list(self.mem['global'].keys())

    def destroy_glob(self, name, persist=True):
        """Destroy global config from session cache then store"""
        self.mem['global'][name] = None
        del self.mem['global'][name]
        if(persist):
            self.destroy_glob_from_store(name)

    def clear_mem_cache(self):
        """
        Clears memory, should only be used if underlying store is modified
        through other means than methods of this class
        """
        mem_hook.__init__(self)

    def get_obj_from_store(self, item_id):
        """
        Get item from externally hooked general store by id
        """

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        return False

    def save_obj_to_store(self, item):
        """Save item to externally hooked general store"""

    def destroy_obj_from_store(self, item):
        """Destroy item to externally hooked general store"""

    def get_glob_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        return False

    def save_glob_to_store(self, name, value):
        """Save global config to externally hooked general store"""

    def list_glob_from_store(self):
        """Get list of global config to externally hooked general store"""

    def destroy_glob_from_store(self, name):
        """Destroy global config to externally hooked general store"""

    def commit(self):
        """Write through all saves to store"""

    # Utilities
    def get_object_distribution(self):
        dist = {}
        for i in self.mem.keys():
            t = type(self.mem[i])
            if(t in dist.keys()):
                dist[t] += 1
            else:
                dist[t] = 1
        return dist
