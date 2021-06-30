from .id_list import id_list
from .utils import logger
import json


def json_str_to_jsci_dict(input_str, owner_obj=None):
    """
    Helper function to convert JSON strings to dictionarys with _ids list
    conversions from hex to UUID

    ret_obj is the owning object for id_list objects
    """
    try:
        obj_fields = json.loads(input_str)
    except ValueError:
        logger.error(
            str(f'Invalid jsci_obj string {input_str} on {owner_obj.id.urn}'))
        obj_fields = {}
    for i in obj_fields.keys():
        if(str(i).endswith("_ids") and isinstance(obj_fields[i], list)):
            obj_fields[i] = id_list(owner_obj, obj_fields[i])
    return obj_fields


class mem_hook():
    """
    Set of virtual functions to be used as hooks to allow access to
    the complete set of items across jaseci object types. This class contains
    a number of blank function calls to be bound extrenally and passed
    to the objects. They return jaseci core types.
    """

    def __init__(self):
        self.mem = {}

    def get_obj(self, item_id):
        """
        Get item from session cache by id, then try store
        """
        if(item_id in self.mem.keys()):
            return self.mem[item_id]
        else:
            ret = self.get_obj_from_store(item_id)
            self.mem[item_id] = ret
            return ret

    def has_obj(self, item_id):
        """
        Checks for object existance
        """
        if(item_id in self.mem.keys()):
            return True
        else:
            return self.has_obj_in_store(item_id)

    def save_obj(self, item, persist=False):
        """Save item to session cache, then to store"""
        self.mem[item.id] = item
        if (persist):
            self.save_obj_to_store(item)

    def destroy_obj(self, item, persist=False):
        """Destroy item from session cache then  store"""
        self.mem[item.id] = None
        del self.mem[item.id]
        if(persist):
            self.destroy_obj_from_store(item)

    def get_cfg(self, name):
        """
        Get global config from session cache by id, then try store
        """
        if(name in self.mem.keys()):
            return self.mem[name]
        else:
            ret = self.get_cfg_from_store(name)
            self.mem[name] = ret
            return ret

    def has_cfg(self, name):
        """
        Checks for global config existance
        """
        if(name in self.mem.keys()):
            return True
        else:
            return self.has_cfg_in_store(name)

    def save_cfg(self, name, value, persist=True):
        """Save global config to session cache, then to store"""
        self.mem[name] = value
        if (persist):
            self.save_cfg_to_store(name, value)

    def destroy_cfg(self, name, persist=True):
        """Destroy global config from session cache then  store"""
        self.mem[name] = None
        del self.mem[name]
        if(persist):
            self.destroy_cfg_from_store(name)

    def get_obj_from_store(self, item_id):
        """
        Get item from externally hooked general store by id
        """
        return None

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        return False

    def save_obj_to_store(self, item):
        """Save item to externally hooked general store"""

    def destroy_obj_from_store(self, item):
        """Destroy item to externally hooked general store"""

    def get_cfg_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        return None

    def has_cfg_in_store(self, name):
        """
        Checks for global config existance in store
        """
        return False

    def save_cfg_to_store(self, name, value):
        """Save global config to externally hooked general store"""

    def destroy_cfg_from_store(self, name):
        """Destroy global config to externally hooked general store"""

    def clear_mem_cache(self):
        """
        Clears memory, should only be used if underlying store is modified
        through other means than methods of this class
        """
        self.mem = {}

    def commit(self):
        """Write through all saves to store"""
