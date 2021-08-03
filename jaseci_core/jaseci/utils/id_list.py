
"""
ID list class for Jaseci

Generalized functions for managing '_ids' convention for lists of Jaseci
objects

owner_obj is the instance that the list belongs to
"""
from jaseci.utils.utils import logger
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

    def get_obj_by_name(self, name, kind=None, silent=False):
        """Returns a Jaseci obj obj by it's name"""
        healing = []
        ret = None
        for i in self:
            if (not self.owner_obj._h.has_obj(uuid.UUID(i))):
                logger.critical(str(
                    f'Self healing: {i} not found ' +
                    f'in id_list of {self.owner_obj}!'))
                healing.append(i)
                continue
            obj = self.owner_obj._h.get_obj(uuid.UUID(i))
            if(obj.name == name):
                if(kind and obj.kind != kind):
                    continue
                ret = self.owner_obj._h.get_obj(uuid.UUID(i))
                break
        self.heal(healing)
        if not silent:
            logger.error(
                str(f"object for '{name}' not found in '{self.owner_obj}'!")
            )
        return ret

    def has_obj_by_name(self, name, kind=None):
        """Returns whether a Jaseci obj exists by it's name"""
        return self.get_obj_by_name(
            name, kind, silent=True
        ) is not None

    def remove_obj_by_name(self, name, kind=None):
        """Remove a Jaseci obj by it's name"""
        self.remove_obj(self.get_obj_by_name(name, kind))

    def destroy_obj_by_name(self, name, kind=None):
        """Destroy a Jaseci obj by it's name"""
        self.destroy_obj(self.get_obj_by_name(name, kind))

    def obj_list(self):
        """Return list of objects from ids"""
        ret = []
        healing = []
        for i in self:
            obj = self.owner_obj._h.get_obj(uuid.UUID(i))
            if (not obj):
                logger.critical(str(
                    f'Self healing: {i} not found ' +
                    f'in id_list of {self.owner_obj}!'))
                healing.append(i)
            else:
                ret.append(self.owner_obj._h.get_obj(uuid.UUID(i)))
        self.heal(healing)
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

    def heal(self, healing):
        if(len(healing)):
            for i in healing:
                self.remove(i)
            self.owner_obj.save()

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
