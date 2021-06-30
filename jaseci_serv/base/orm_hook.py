"""
This module includes code related to hooking Jaseci's django models to the
core engine.
"""
from django.core.exceptions import ObjectDoesNotExist

from jaseci.utils import utils
from jaseci.utils.utils import logger
import jaseci as core_mod
from jaseci.utils.mem_hook import mem_hook, json_str_to_jsci_dict
from jaseci_serv.settings import REDIS_HOST
from redis import Redis
import uuid
import json


class orm_hook(mem_hook):
    """
    Hooks Django ORM database for Jaseci objects to Jaseci's core engine.

    Sets user on initialization to route calls to correct user. This hook
    lives in :class:`User` class as per :field:`User.orm_hook`.
    """

    def __init__(self, user, objects, configs,
                 red=Redis(host=REDIS_HOST, decode_responses=True)):
        self.user = user
        self.objects = objects
        self.configs = configs
        self.red = red
        self.save_obj_list = set()
        self.save_cfg_list = []
        super().__init__()

    def get_obj_from_store(self, item_id):
        loaded_obj = self.red.get(item_id.urn)
        if (loaded_obj):
            j_type = json.loads(loaded_obj)['j_type']
            class_for_type = \
                utils.find_class_and_import(j_type, core_mod)
            ret_obj = class_for_type(h=self, auto_save=False)
            ret_obj.json_load(loaded_obj)

            return ret_obj
        else:
            try:
                loaded_obj = self.objects.get(user=self.user, jid=item_id)
            except ObjectDoesNotExist:
                logger.error(
                    str(f"Object {item_id} does not exist in Django ORM!"),
                    exc_info=True
                )
                return None

            class_for_type = \
                utils.find_class_and_import(loaded_obj.j_type, core_mod)
            ret_obj = class_for_type(h=self, auto_save=False)
            utils.map_assignment_of_matching_fields(ret_obj, loaded_obj)
            assert(uuid.UUID(ret_obj.jid) == loaded_obj.jid)

            # Unwind jsci_payload for fields beyond element object
            obj_fields = json_str_to_jsci_dict(loaded_obj.jsci_obj, ret_obj)
            for i in obj_fields.keys():
                setattr(ret_obj, i, obj_fields[i])

            self.red.set(ret_obj.id.urn, ret_obj.json(detailed=True))
            return ret_obj

    def has_obj_in_store(self, item_id):
        """
        Checks for object existance in store
        """
        if (self.red.get(item_id.urn)):
            return True
        return self.objects.filter(jid=item_id).count()

    def save_obj_to_store(self, item):
        # import traceback as tb; tb.print_stack();  # noqa
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
        item_from_db, created = self.objects.get_or_create(
            user=self.user, jid=item.id
        )
        utils.map_assignment_of_matching_fields(item_from_db, item)
        item_from_db.jsci_obj = item.jsci_payload()
        item_from_db.save()

    def destroy_obj_from_store(self, item):
        try:
            self.objects.get(user=self.user, jid=item.id).delete()
        except ObjectDoesNotExist:
            # NOTE: Should look at this at some point
            # logger.error("Object does not exists so delete aborted!")
            pass
        self.red.delete(item.id.urn)

    def get_cfg_from_store(self, name):
        """
        Get global config from externally hooked general store by name
        """
        loaded_val = self.red.get(name)
        if (loaded_val):
            return loaded_val
        else:
            try:
                loaded_val = self.configs.get(name=name).value
            except ObjectDoesNotExist:
                logger.error(
                    str(f"Config {name} does not exist in Django ORM!"),
                    exc_info=True
                )
                return None

            self.red.set(name, loaded_val)
            return loaded_val

    def has_cfg_in_store(self, name):
        """
        Checks for global config existance in store
        """
        if (self.red.get(name)):
            return True
        return self.configs.filter(name=name).count()

    def save_cfg_to_store(self, name, value):
        """Save global config to externally hooked general store"""
        self.save_cfg_list.append([name, value])

    def destroy_cfg_from_store(self, name):
        """Destroy global config to externally hooked general store"""
        try:
            self.configs.get(name=name).delete()
        except ObjectDoesNotExist:
            pass
        self.red.delete(name)

    def commit_cfg(self, name, value):
        try:
            self.red.set(name, value)
        except Exception as e:
            logger.error(
                str(f"Couldn't save {name} to redis! {e}"),
                exc_info=True
            )
        item_from_db, created = self.configs.get_or_create(name=name)
        item_from_db.value = value
        item_from_db.save()

    def commit(self):
        """Write through all saves to store"""
        # dist = {}
        # for i in self.save_obj_list:
        #     if (type(i).__name__ in dist.keys()):
        #         dist[type(i).__name__] += 1
        #     else:
        #         dist[type(i).__name__] = 1
        # print(dist)
        for i in self.save_obj_list:
            self.commit_obj(i)
        self.save_obj_list = set()
        for i in self.save_cfg_list:
            self.commit_cfg(name=i[0], value=i[1])
        self.save_cfg_list = []
