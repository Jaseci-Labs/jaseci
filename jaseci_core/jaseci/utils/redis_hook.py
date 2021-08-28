"""
This module includes code related to hooking Jaseci's Redis to the
core engine.
"""
from jaseci.utils import utils
from jaseci.utils.utils import logger
import jaseci as core_mod
from jaseci.utils.mem_hook import mem_hook
from redis import Redis
import json


class redis_hook(mem_hook):
    """
    Hooks Django ORM database for Jaseci objects to Jaseci's core engine.

    Sets user on initialization to route calls to correct user. This hook
    lives in :class:`User` class as per :field:`User.orm_hook`.
    """

    def __init__(self, red=Redis()):
        self.red = red
        self.save_obj_list = set()
        self.save_glob_dict = {}
        super().__init__()

    def get_obj_from_store(self, item_id):
        loaded_obj = self.red.get(item_id.urn)
        if(not loaded_obj):
            logger.error(
                str(f"Object {item_id} does not exist in Redis!")
            )
            return None

        jdict = json.loads(loaded_obj)
        j_type = jdict['j_type']
        j_master = jdict['j_master']
        class_for_type = \
            utils.find_class_and_import(j_type, core_mod)
        ret_obj = class_for_type(h=self, m_id=j_master, auto_save=False)
        ret_obj.json_load(loaded_obj)

        return ret_obj

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        if (self.red.exists(item_id.urn)):
            return True
        return False

    def save_obj_to_store(self, item):
        self.save_obj_list.add(item)

    def commit_obj(self, item):
        try:
            self.red.set(item.id.urn, item.json(detailed=True))
        except TypeError:
            logger.error(
                str(f"Item {item} is not JSON serializable for redis store!"),
                exc_info=True
            )
        except Exception as e:
            logger.error(
                str(f"Couldn't save {item} to redis! {e}"),
                exc_info=True
            )

    def destroy_obj_from_store(self, item):
        self.red.delete(item.id.urn)
        if(item in self.save_obj_list):
            self.save_obj_list.remove(item)

    def get_glob_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        loaded_val = self.red.get(name)
        if (loaded_val):
            return loaded_val
        else:
            logger.error(
                str(f"Global {name} does not exist in Django ORM!"),
                exc_info=True
            )
            return None

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        if (self.red.exists(name)):
            return True
        return False

    def save_glob_to_store(self, name, value):
        """Save global config to externally hooked general store"""
        self.save_glob_dict[name] = value

    def list_glob_from_store(self):
        """Get list of globals to externally hooked general store"""
        logger.warning(str(f"Globals can not (yet) be listed from Redis!"))
        return []

    def destroy_glob_from_store(self, name):
        """Destroy global config to externally hooked general store"""
        self.red.delete(name)
        if(name in self.save_glob_dict.keys()):
            del self.save_glob_dict[name]

    def commit_glob(self, name, value):
        try:
            self.red.set(name, value)
        except Exception as e:
            logger.error(
                str(f"Couldn't save {name} to redis! {e}"),
                exc_info=True
            )

    def commit(self):
        """Write through all saves to store"""
        for i in self.save_obj_list:
            self.commit_obj(i)
        self.save_obj_list = set()
        for i in self.save_glob_dict.keys():
            self.commit_glob(name=i, value=self.save_glob_dict[i])
        self.save_glob_dict = {}
