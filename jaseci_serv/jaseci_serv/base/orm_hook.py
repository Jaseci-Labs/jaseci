"""
This module includes code related to hooking Jaseci's django models to the
core engine.

FIX: Serious permissions work needed
"""
from django.core.exceptions import ObjectDoesNotExist

from jaseci.utils import utils
from jaseci.utils.utils import logger
import jaseci as core_mod
from jaseci.utils.mem_hook import mem_hook, json_str_to_jsci_dict
from jaseci_serv. jaseci_serv.settings import REDIS_HOST
from redis import Redis
import uuid
import json


def find_class_and_import(j_type, core_mod):
    if(j_type == 'master'):
        from jaseci_serv.base.models import master
        return master
    elif(j_type == 'super_master'):
        from jaseci_serv.base.models import super_master
        return super_master
    else:
        return utils.find_class_and_import(j_type, core_mod)


class orm_hook(mem_hook):
    """
    Hooks Django ORM database for Jaseci objects to Jaseci's core engine.
    """

    def __init__(self, objects, globs,
                 red=Redis(host=REDIS_HOST, decode_responses=True)):
        self.objects = objects
        self.globs = globs
        self.red = red
        self.skip_redis_update = False
        self.save_obj_list = set()
        self.save_glob_dict = {}
        super().__init__()

    def get_obj_from_store(self, item_id):
        loaded_obj = self.red.get(item_id.urn)
        if (loaded_obj):
            jdict = json.loads(loaded_obj)
            j_type = jdict['j_type']
            j_master = jdict['j_master']
            class_for_type = \
                find_class_and_import(j_type, core_mod)
            ret_obj = class_for_type(
                h=self, m_id=j_master, auto_save=False)
            ret_obj.json_load(loaded_obj)

            return ret_obj
        else:
            try:
                loaded_obj = self.objects.get(
                    jid=item_id)
            except ObjectDoesNotExist:
                logger.error(
                    str(f"Object {item_id} does not exist in Django ORM!"),
                    exc_info=True
                )
                return None

            class_for_type = \
                find_class_and_import(loaded_obj.j_type, core_mod)
            ret_obj = class_for_type(
                h=self, m_id=loaded_obj.j_master, auto_save=False)
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

    def commit_obj_to_redis(self, item):
        try:
            self.red.set(item.id.urn, item.json(detailed=True))
        except TypeError:
            logger.error(
                f"Item {item} is not JSON serializable for redis store!")
            logger.error(f"Item details: {item.serialize()}",  exc_info=True)
        except Exception as e:
            logger.error(
                str(f"Couldn't save {item} to redis! {e}"),
                exc_info=True
            )

    def commit_obj(self, item):
        item_from_db, created = self.objects.get_or_create(jid=item.id
                                                           )
        utils.map_assignment_of_matching_fields(item_from_db, item)
        item_from_db.jsci_obj = item.jsci_payload()
        item_from_db.save()

    def destroy_obj_from_store(self, item):
        try:
            self.objects.get(jid=item.id).delete()
        except ObjectDoesNotExist:
            # NOTE: Should look at this at some point
            # logger.error("Object does not exists so delete aborted!")
            pass
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
            try:
                loaded_val = self.globs.get(name=name).value
            except ObjectDoesNotExist:
                logger.error(
                    str(f"Global {name} does not exist in Django ORM!"),
                    exc_info=True
                )
                return None

            self.red.set(name, loaded_val)
            return loaded_val

    def has_glob_in_store(self, name):
        """
        Checks for global config existance in store
        """
        if (self.red.get(name)):
            return True
        return self.globs.filter(name=name).count()

    def save_glob_to_store(self, name, value):
        """Save global config to externally hooked general store"""
        self.save_glob_dict[name] = value

    def list_glob_from_store(self):
        """Get list of global config to externally hooked general store"""
        return [entry['name'] for entry in self.globs.values('name')]

    def destroy_glob_from_store(self, name):
        """Destroy global config to externally hooked general store"""
        try:
            self.globs.get(name=name).delete()
        except ObjectDoesNotExist:
            pass
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
        item_from_db, created = self.globs.get_or_create(name=name)
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
            if(not self.skip_redis_update):
                self.commit_obj_to_redis(i)
            else:
                self.skip_redis_update = False
            self.commit_obj(i)
        self.save_obj_list = set()
        for i in self.save_glob_dict.keys():
            self.commit_glob(name=i, value=self.save_glob_dict[i])
        self.save_glob_dict = {}
