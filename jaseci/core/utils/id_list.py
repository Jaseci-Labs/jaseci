
"""
ID list class for Jaseci

Generalized functions for managing '_ids' convention for lists of Jaseci
objects

owner_obj is the instance that the list belongs to
"""
from core.utils.utils import logger
import uuid


class id_list(list):
    """
    ID list class for tracking lists of objects in Jaseci

    ingest_list is a list of hex strings to convert to UUID and append.
    """

    def __init__(self, owner_obj, in_list=None):
        self.owner_obj = owner_obj
        if (in_list):
            for i in in_list:
                self.append(i)

    def add_obj(self, obj, silent=False):
        """Adds a obj obj to Jaseci object"""
        self.owner_obj.check_hooks_match(obj)
        if obj.jid in self and not silent:
            logger.warning(
                str(f"{obj} is already in {self.owner_obj}'s list")
            )
        else:
            self.append(obj.jid)
            if(not obj.owner_id):
                obj.owner_id = self.owner_obj.id
            obj.save()
            self.owner_obj.save()

    def remove_obj(self, obj):
        """Remove a Jaseci obj from list"""
        self.remove(obj.jid)
        self.owner_obj.save()

    def destroy_obj(self, obj):
        """Completely destroys a Jaseci obj obj by it's name"""
        self.remove_obj(obj)
        obj.destroy()

    def get_obj_by_name(self, name, silent=False):
        """Returns a Jaseci obj obj by it's name"""
        for i in self:
            if(not self.owner_obj._h.has_obj(uuid.UUID(i))):
                break
            if(self.owner_obj._h.get_obj(uuid.UUID(i)).name == name):
                return self.owner_obj._h.get_obj(uuid.UUID(i))
        if not silent:
            logger.error(
                str(f"object for '{name}' not found in '{self.owner_obj}'!")
            )
        return None

    def has_obj_by_name(self, name):
        """Returns whether a Jaseci obj exists by it's name"""
        return self.get_obj_by_name(
            name, silent=True
        ) is not None

    def remove_obj_by_name(self, name):
        """Remove a Jaseci obj by it's name"""
        self.remove_obj(self.get_obj_by_name(name))

    def destroy_obj_by_name(self, name):
        """Destroy a Jaseci obj by it's name"""
        self.destroy_obj(self.get_obj_by_name(name))

    def obj_list(self):
        """Return list of objects from ids"""
        ret = []
        for i in self:
            obj = self.owner_obj._h.get_obj(uuid.UUID(i))
            if (not obj):
                logger.critical(str(
                    f'Self healing: {i} not found ' +
                    f'in id_list of {self.owner_obj}!'))
                self.remove(i)
                self.owner_obj.save()
            else:
                ret.append(self.owner_obj._h.get_obj(uuid.UUID(i)))
        return ret

    def remove_all(self):
        """Remove a Jaseci obj obj by it's name"""
        for i in self.obj_list():
            self.remove_obj(i)
        if (len(self)):
            logger.critical(str(
                f'Removeall all failed in id_list of {self.owner_obj} - ' +
                f'still has {self}!'))

    def destroy_all(self):
        """Remove a Jaseci obj obj by it's name"""
        for i in self.obj_list():
            self.destroy_obj(i)
        if (len(self)):
            logger.critical(str(
                f'Destroy all failed in id_list of {self.owner_obj} - ' +
                f'still has {self}!'))

    def first_obj(self):
        """Get first object in list"""
        if(not self):
            logger.error(
                str(f"List in '{self.owner_obj}' is empty!")
            )
            return None
        return self.owner_obj._h.get_obj(uuid.UUID(self[0]))

    def pop_first_obj(self):
        """Get first object in list"""
        ret = self.first_obj()
        if(ret):
            self.remove_obj(ret)
        return ret
