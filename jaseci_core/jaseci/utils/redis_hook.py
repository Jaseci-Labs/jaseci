"""
This module includes code related to hooking Jaseci's Redis to the
core engine.
"""
import jaseci as core_mod
from jaseci.utils.utils import logger
from jaseci.utils.mem_hook import mem_hook
from redis import Redis, RedisError
import json

from .json_handler import JaseciJsonDecoder


class redis_hook(mem_hook):

    app: Redis = None
    no_error = True

    def __init__(
        self, redis_enabled=True, redis_host="localhost", redis_port=6379, redis_db=0
    ):
        try:
            if redis_enabled and rh.no_error and rh.app is None:
                rh.app = Redis(
                    host=redis_host, port=redis_port, db=redis_db, decode_responses=True
                )
                rh.app.ping()

        except RedisError as e:
            logger.error(
                f"Skipping Redis due to initialization failure! Error: '{str(e)}'"
            )

            rh.app = None
            rh.no_error = False

        super().__init__()

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def is_running():
        return not (rh.app is None)

    def clear_mem_cache(self):
        """
        Clears memory, should only be used if underlying store is modified
        through other means than methods of this class
        """
        if rh.is_running():
            rh.app.flushdb()
        redis_hook.__init__(self)

    ####################################################
    #        DATASOURCE METHOD (TO BE OVERRIDE)        #
    ####################################################

    # --------------------- OBJ ---------------------- #

    def get_obj_from_store(self, item_id):
        """
        Get item from externally hooked general store by id
        """
        obj = super().get_obj_from_store(item_id)

        if obj is None and rh.is_running():
            loaded_obj = rh.app.get(item_id.urn)
            if loaded_obj:
                jdict = json.loads(loaded_obj, cls=JaseciJsonDecoder)
                j_type = jdict["j_type"]
                j_master = jdict["j_master"]
                class_for_type = self.find_class_and_import(j_type, core_mod)
                ret_obj = class_for_type(h=self, m_id=j_master, auto_save=False)
                ret_obj.json_load(loaded_obj)

                super().commit_obj_to_cache(ret_obj)
                return ret_obj

        return obj

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        return super().has_obj_in_store(item_id) or (
            rh.is_running() and rh.app.exists(item_id.urn)
        )

    # --------------------- GLOB --------------------- #

    def get_glob_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        glob = super().get_glob_from_store(name)

        if glob is None and rh.is_running():
            glob = rh.app.get(name)

            if glob:
                super().commit_glob_to_cache(name, glob)

        return glob

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        return super().has_glob_in_store(name) or (
            rh.is_running() and rh.app.exists(name)
        )

    def list_glob_from_store(self):
        """Get list of global config to externally hooked general store"""
        globs = super().list_glob_from_store()

        if not globs and rh.is_running():
            logger.warning("Globals can not (yet) be listed from Redis!")
            return []

        return globs

    ###################################################
    #   CACHE CONTROL (SHOULD NOT OVERRIDEN ON ORM)   #
    ###################################################

    # -------------------- GLOBS -------------------- #

    def commit_glob_to_cache(self, name, value):
        super().commit_glob_to_cache(name, value)

        if rh.is_running():
            rh.app.set(name, value)

    def decommit_glob_from_cache(self, name):
        super().decommit_glob_from_cache(name)

        if rh.is_running():
            rh.app.delete(name)

    # --------------------- OBJ --------------------- #

    def commit_obj_to_cache(self, item):
        super().commit_obj_to_cache(item)

        if rh.is_running():
            rh.app.set(item.id.urn, item.json(detailed=True))

    def decommit_obj_from_cache(self, item):
        super().decommit_obj_from_cache(item)

        if rh.is_running():
            rh.app.delete(item.id.urn)


rh = redis_hook
