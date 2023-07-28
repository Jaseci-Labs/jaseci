"""
ID list class for Jaseci

Generalized functions for managing '_ids' convention for lists of Jaseci
objects

parent_obj is the instance that the list belongs to
"""
from jaseci.utils.utils import logger


class IdList(list):
    """
    ID list class for tracking lists of objects in Jaseci

    ingest_list is a list of hex strings to convert to UUID and append.
    """

    def __init__(self, parent_obj, auto_save=True, in_list=None):
        self.parent_obj = parent_obj
        self.cached_objects = []
        self.heal_list = []
        self.auto_save = auto_save
        if in_list:
            self.extend(in_list)

    def cache_reset(self):
        self.cached_objects = []

    def add_obj(
        self, obj, push_front=False, allow_dups=False, silent=False, bypass=False
    ):
        """Adds a obj obj to Jaseci object"""
        self.parent_obj.check_hooks_match(obj)
        if not allow_dups and obj.jid in self:
            if not silent:
                logger.warning(str(f"{obj} is already in {self.parent_obj}'s list"))
        else:
            self.cache_reset()
            if push_front:
                self.insert(0, obj.jid)
            else:
                self.append(obj.jid)

            if not bypass:
                if not obj.j_parent:
                    obj.j_parent = self.parent_obj.jid
                    self.save(obj)
                self.save()

    def add_obj_list(self, obj_list, push_front=False, allow_dups=False, silent=False):
        self.cache_reset()
        if push_front:
            obj_list.reverse()
        for i in obj_list:
            self.add_obj(i, push_front=push_front, allow_dups=allow_dups, silent=silent)

    def remove_obj(self, obj):
        """Remove a Jaseci obj from list"""
        self.cache_reset()
        self.remove(obj.jid)
        self.save()

    def heal(self):
        for i in self.heal_list:
            self.remove(i)
        if len(self.heal_list) and hasattr(self.parent_obj, "save"):
            self.save()
        self.heal_list = []

    def destroy_obj(self, obj):
        """Completely destroys a Jaseci obj obj by it's name"""
        self.remove_obj(obj)
        obj.destroy()

    def obj_for_id_not_exist_error(self, item_id):
        self.heal_list.append(item_id)
        my_name = "id_list"
        for k, v in self.parent_obj.__dict__.items():
            if id(v) == id(self):
                my_name = k
        return f"{item_id} not found in {my_name} of {self.parent_obj}!"

    def get_obj_by_name(self, name, kind=None, silent=False):
        """Returns a Jaseci obj obj by it's name"""
        ret = None
        for i in self:
            obj = self.parent_obj._h.get_obj(self.parent_obj._m_id, i)
            if not obj:
                logger.critical(self.obj_for_id_not_exist_error(i))
                continue
            if obj.name == name:
                if kind and obj.kind != kind:
                    continue
                ret = obj
                break
        if not ret and not silent:
            logger.error(str(f"object for '{name}' not found in '{self.parent_obj}'!"))
        self.heal()
        return ret

    def has_obj_by_name(self, name, kind=None):
        """Returns whether a Jaseci obj exists by it's name"""
        return self.get_obj_by_name(name, kind, silent=True) is not None

    def remove_obj_by_name(self, name, kind=None):
        """Remove a Jaseci obj by it's name"""
        self.remove_obj(self.get_obj_by_name(name, kind))

    def destroy_obj_by_name(self, name, kind=None):
        """Destroy a Jaseci obj by it's name"""
        self.destroy_obj(self.get_obj_by_name(name, kind))

    def obj_list(self):
        """Return list of objects from ids"""
        if not len(self.cached_objects):
            for i in self:
                obj = self.parent_obj._h.get_obj(self.parent_obj._m_id, i)
                if not obj:
                    logger.critical(self.obj_for_id_not_exist_error(i))
                else:
                    self.cached_objects.append(obj)
        self.heal()
        return self.cached_objects.copy()

    def remove_all(self):
        """Remove a Jaseci obj obj by it's name"""
        for i in self.obj_list():
            self.remove_obj(i)
        if len(self):
            logger.critical(
                str(
                    f"Remove all failed in id_list of {self.parent_obj} - "
                    + f"still has {self}!"
                )
            )

    def destroy_all(self):
        """Remove a Jaseci obj obj by it's name"""
        for i in self.obj_list():
            self.destroy_obj(i)
        if len(self):
            logger.critical(
                str(
                    f"Destroy all failed in id_list of {self.parent_obj} - "
                    + f"still has {self}!"
                )
            )

    def first_obj(self):
        """Get first object in list"""
        if not self:
            logger.error(str(f"List in '{self.parent_obj}' is empty!"))
            return None
        return self.parent_obj._h.get_obj(self.parent_obj._m_id, self[0])

    def pop_first_obj(self):
        """Get first object in list"""
        ret = self.first_obj()
        if ret:
            self.remove_obj(ret)
        return ret

    def save(self, obj=None):
        if self.auto_save:
            self.parent_obj.save()
        if obj:
            obj.save()
