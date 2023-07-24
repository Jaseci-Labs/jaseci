from json import dumps, loads
import sys
from jaseci.utils.file_handler import FileHandler
from jaseci.utils.utils import find_class_and_import
from jaseci.jsorc.jsorc import JsOrc


@JsOrc.repository(name="hook")
class MemoryHook:
    """
    Set of virtual functions to be used as hooks to allow access to
    the complete set of items across jaseci object types. This class contains
    a number of blank function calls to be bound extrenally and passed
    to the objects. They return jaseci core types.
    """

    def __init__(self):
        from jaseci.jsorc.live_actions import get_global_actions

        self.mem = {"global": {}}
        self._machine = None
        self.save_obj_list = set()
        self.save_glob_dict = {}
        self.file_handlers = {}

    ####################################################
    #               COMMON GETTER/SETTER               #
    ####################################################

    # --------------------- OBJ ---------------------- #

    def get_obj(self, caller_id, item_id, override=False):
        """
        Get item from session cache by id, then try store
        TODO: May need to make this an object copy so you cant do mem writes
        """
        ret = self.get_obj_from_store(item_id)
        if override or (ret is not None and ret.check_read_access(caller_id)):
            return ret

    def has_obj(self, item_id):
        """
        Checks for object existance
        """
        return self.has_obj_in_store(item_id)

    def save_obj(self, caller_id, item, all_caches=False):
        """Save item to session cache, then to store"""
        if item.check_write_access(caller_id):
            self.commit_obj_to_cache(item, all_caches=all_caches)
            if item._persist:
                self.save_obj_list.add(item)

    def destroy_obj(self, caller_id, item):
        """Destroy item from session cache then  store"""
        if item.check_write_access(caller_id):
            self.decommit_obj_from_cache(item)
            if item._persist:
                self.destroy_obj_from_store(item)

    # --------------------- GLOB --------------------- #

    def get_glob(self, name):
        """
        Get global config from session cache by id, then try store
        """
        return self.get_glob_from_store(name)

    def has_glob(self, name):
        """
        Checks for global config existance
        """
        return self.has_glob_in_store(name)

    def resolve_glob(self, name, default=None):
        """
        Util function for returning config if exists otherwise default
        """
        if self.has_glob(name):
            return self.get_glob(name)
        else:
            return default

    def save_glob(self, name, value, persist=True):
        """Save global config to session cache, then to store"""
        self.commit_glob_to_cache(name, value)

        if persist:
            self.save_glob_dict[name] = value

    def list_glob(self):
        """Lists all configs present"""
        return self.list_glob_from_store()

    def destroy_glob(self, name, persist=True):
        """Destroy global config from session cache then store"""
        self.decommit_glob_from_cache(name)

        if persist:
            self.destroy_glob_from_store(name)

    # ----------------- SERVICE GLOB ----------------- #

    def get_or_create_glob(self, name, val):
        if not self.has_glob(name):
            self.save_glob(name, dumps(val))
            self.commit()
        return loads(self.get_glob(name))

    ####################################################
    #        DATASOURCE METHOD (TO BE OVERRIDE)        #
    ####################################################

    # --------------------- OBJ ---------------------- #

    def get_obj_from_store(self, item_id):
        """
        Get item from externally hooked general store by id
        """
        if item_id in self.mem:
            return self.mem[item_id]

        return None

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        return item_id in self.mem

    def destroy_obj_from_store(self, item):
        """Destroy item to externally hooked general store"""
        if item in self.save_obj_list:
            self.save_obj_list.remove(item)

    # --------------------- GLOB --------------------- #

    def get_glob_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        if name in self.mem["global"]:
            return self.mem["global"][name]

        return None

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        return name in self.mem["global"]

    def destroy_glob_from_store(self, name):
        """Destroy global config to externally hooked general store"""
        if name in self.save_glob_dict:
            self.save_glob_dict.pop(name)

    def list_glob_from_store(self):
        """Get list of global config to externally hooked general store"""
        return list(self.mem["global"].keys())

    ####################################################
    # ------------------ COMMITTER ------------------- #
    ####################################################

    def commit(self, skip_cache=False):
        if not skip_cache:
            for i in self.save_obj_list:
                self.commit_obj_to_cache(i)

            self.save_obj_list = set()

            for i in self.save_glob_dict.keys():
                self.commit_glob_to_cache(name=i, value=self.save_glob_dict[i])

            self.save_glob_dict = {}

    ###################################################
    #   CACHE CONTROL (SHOULD NOT OVERRIDEN ON ORM)   #
    ###################################################

    # -------------------- GLOBS -------------------- #

    def commit_glob_to_cache(self, name, value):
        self.mem["global"][name] = value

    def decommit_glob_from_cache(self, name):
        self.mem["global"].pop(name)

    # --------------------- OBJ --------------------- #

    def has_id_in_mem_cache(self, id):
        return id is not None and id in self.mem

    def commit_obj_to_cache(self, item, all_caches=False):
        self.mem[item.jid] = item

    def commit_all_cache_sync(self):
        for i in self.save_obj_list:
            self.commit_obj_to_cache(i, all_caches=True)

    def decommit_obj_from_cache(self, item):
        self.mem.pop(item.jid)

    ####################################################
    # ------------------ UTILITIES ------------------- #
    ####################################################

    def get_object_distribution(self):
        dist = {}
        for i in self.mem.keys():
            t = type(self.mem[i])
            if t in dist.keys():
                dist[t] += 1
            else:
                dist[t] = 1
        return dist

    def mem_size(self):
        return sys.getsizeof(self.mem) / 1024

    ###################################################
    #                  CLASS CONTROL                  #
    ###################################################

    def find_class_and_import(self, j_type, mod):
        cls = JsOrc.ctx_cls(j_type)

        if not cls:
            cls = find_class_and_import(j_type, mod)

        return cls

    def clear_cache(self):
        MemoryHook.__init__(self)

    ####################################################
    #                   FILE HANDLER                   #
    ####################################################

    def add_file_handler(self, file_handler: FileHandler) -> str:
        self.file_handlers.update({file_handler.id: file_handler})
        return file_handler.id

    def get_file_handler(self, file_id: str):
        return self.file_handlers.get(file_id, None)

    def pop_file_handler(self, file_id: str):
        return self.file_handlers.pop(file_id, None)

    def clean_file_handler(self):
        for file_handler in list(self.file_handlers.values()):
            self.file_handlers.pop(file_handler.id, None)
            if not file_handler.persist:
                file_handler.delete()

    def __del__(self):
        self.clean_file_handler()
