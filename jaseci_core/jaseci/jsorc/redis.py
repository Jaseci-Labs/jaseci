"""
This module includes code related to hooking Jaseci's Redis to the
core engine.
"""
import json

import jaseci as core_mod
from jaseci.utils.json_handler import JaseciJsonDecoder, jsci_dict_normalize
from jaseci.jsorc.memory import MemoryHook
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.redis_svc import RedisService


#################################################
#                  REDIS HOOK                   #
#################################################


@JsOrc.repository(name="hook", priority=1)
class RedisHook(MemoryHook):
    def __init__(self, redis: RedisService = None):
        self.redis = JsOrc.svc("redis", RedisService)
        self.red_touch_count = 0

        super().__init__()

    ####################################################
    #        DATASOURCE METHOD (TO BE OVERRIDE)        #
    ####################################################

    # --------------------- OBJ ---------------------- #

    def get_obj_from_store(self, item_id):
        """
        Get item from externally hooked general store by id
        """
        obj = super().get_obj_from_store(item_id)

        if obj is None and self.redis.is_running():
            loaded_obj = self.redis.get(item_id)
            if loaded_obj:
                self.red_touch_count += 1
                jdict = json.loads(loaded_obj, cls=JaseciJsonDecoder)
                j_type = jdict["j_type"]
                j_master = jdict["j_master"]
                class_for_type = self.find_class_and_import(j_type, core_mod)
                ret_obj = class_for_type(h=self, m_id=j_master, auto_save=False)
                jsci_dict_normalize(jdict, parent_obj=ret_obj)
                ret_obj.dict_load(jdict)

                super().commit_obj_to_cache(ret_obj)
                obj = ret_obj
        if obj:
            obj._persist = True
        return obj

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        return super().has_obj_in_store(item_id) or (
            self.redis.is_running() and self.redis.exists(item_id)
        )

    # --------------------- GLOB --------------------- #

    def get_glob_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        glob = super().get_glob_from_store(name)

        if glob is None and self.redis.is_running():
            glob = self.redis.hget("global", name)

            if glob:
                self.red_touch_count += 1
                super().commit_glob_to_cache(name, glob)

        return glob

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        return super().has_glob_in_store(name) or (
            self.redis.is_running() and self.redis.hexists("global", name)
        )

    def list_glob_from_store(self):
        """Get list of global config to externally hooked general store"""
        globs = super().list_glob_from_store()

        if not globs and self.redis.is_running():
            globs = self.redis.hkeys("global")

        return globs

    ###################################################
    #   CACHE CONTROL (SHOULD NOT OVERRIDEN ON ORM)   #
    ###################################################

    # -------------------- GLOBS -------------------- #

    def commit_glob_to_cache(self, name, value):
        super().commit_glob_to_cache(name, value)
        if self.redis.is_running():
            self.redis.hset("global", name, value)

    def decommit_glob_from_cache(self, name):
        super().decommit_glob_from_cache(name)

        if self.redis.is_running():
            self.redis.hdel("global", name)

    # --------------------- OBJ --------------------- #

    def commit_obj_to_cache(self, item, all_caches=False):
        super().commit_obj_to_cache(item)

        if all_caches and item._persist and self.redis.is_running():
            self.redis.set(item.jid, item.json(detailed=True))

    def decommit_obj_from_cache(self, item):
        super().decommit_obj_from_cache(item)

        if item._persist and self.redis.is_running():
            self.redis.delete(item.jid)

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def clear_cache(self):
        if self.redis.is_running():
            self.redis.app.flushdb()

        MemoryHook.__init__(self)


# ----------------------------------------------- #
