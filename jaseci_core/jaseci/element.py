"""
Base Jaseci object class

Naming conventions
* '_ids', '_id' - appended to lists of ids as feilds of jaseci objects
* 'obj' - used to represent a jaseci object
* 'item' - Items are kv pairs derived from item class, dont use elsewhere
* 'store' - refers to persistent store for hooks from engine, (dont use db)
"""

import uuid
from datetime import datetime
import copy
import json
from jaseci.utils.utils import logger
from jaseci.utils.id_list import id_list
from jaseci.utils.mem_hook import mem_hook
from jaseci.utils.mem_hook import json_str_to_jsci_dict


__version__ = '1.0.0'


class ctx_value():
    """A reference into the context dict that is common for elements"""

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name


class anchored():
    """Utility class for objects that hold anchor values"""

    def __init__(self):
        self.anchor = None

    def anchor_value(self):
        """Returns value of anchor context object"""
        if(self.anchor):
            return self.context[self.anchor]
        return None


class hookable():
    """Utility class for objects that are savable to DBs and other stores"""

    def __init__(self, h: mem_hook, persist: bool = True):
        self._h = h  # hook for storing and loading to persistent store
        self._persist = persist

    def check_hooks_match(self, target, silent=False):
        """Checks whether target object hook matches self's hook"""
        if(not silent and target._h != self._h):
            logger.critical(str("Hook for {} does not match {}".
                                format(target, self)))
        return target._h == self._h

    def save(self):
        """
        Write self through hook to persistent storage
        """
        self._h.save_obj(self, self._persist)

    def destroy(self):
        """
        Destroys self from persistent storage

        Note that the object will still exist in python until GC'd
        """
        self._h.destroy_obj(self, self._persist)
        del self

    def owner(self):
        """
        Returns the objects for list of owners of this element
        """
        return self._h.get_obj(self.owner_id)


class element(hookable):
    """
    Base class for Jaseci for standard info shared across all objects types in
    Jaseci. This class also includes a method for dumping the non-general items
    as a single dictionary. The :meth:`jsci_payload` function automatically
    finds relevant non general fields and returns a dictionary of them.

    Keep in mind that when a valid hook is passed, the item writes itself on
    creation.

    Auto save should be faulse when loading from database so a new UUID is
    not randomly created and saved back to db on load

    TODO: Make below content a documentation variable and link in a few places
    Keep in mind the postfix of '_ids' on feilds of derived classes of element
    is a Jaseci convention for lists of uuids that are stored as hex and loaded
    as type UUID.

    NOTE: All fields of elements and it's derived classes are assumed to be
    json serializable types
    """

    def __init__(self, h, owner_id=None, name='basic', kind='generic',
                 user='Anonymous', has_access=[], auto_save=True, *args,
                 **kwargs):
        self.name = name
        self.kind = kind
        self.jid = uuid.uuid4().urn
        self.j_owner = owner_id.urn if owner_id else None  # member of
        self.j_timestamp = datetime.utcnow().isoformat()
        self.j_type = type(self).__name__
        # self.j_user = user  # TODO: Finish this permissions approach
        # self.j_has_access = has_access
        hookable.__init__(self, h,  *args, **kwargs)
        if(auto_save):
            self.save()

    @property
    def id(self):
        return uuid.UUID(self.jid)

    @id.setter
    def id(self, obj):
        self.jid = obj.urn

    @property
    def owner_id(self) -> uuid.UUID:
        if (not self.j_owner):
            return None
        return uuid.UUID(self.j_owner)

    @owner_id.setter
    def owner_id(self, obj: uuid.UUID):
        if (not obj):
            self.j_owner = None
        else:
            self.j_owner = obj.urn

    @property
    def timestamp(self):
        return datetime.fromisoformat(self.j_timestamp)

    @timestamp.setter
    def timestamp(self, obj):
        self.j_timestamp = obj.isoformat()

    def duplicate(self, persist_dup: bool = True):
        """
        Duplicates elements by creating copy with new id
        Hook override to duplicate into mem / another store
        """

        dup = type(self)(h=self._h, persist=persist_dup)
        id_save = dup.id
        dup.json_load(self.json())
        dup.id = id_save
        dup.timestamp = datetime.utcnow()
        dup.save()
        return dup

    def is_equivalent(self, obj):
        """
        Duplicates elements by creating copy with new id
        """
        if(self.j_type != obj.j_type):
            return False
        for i in vars(self).keys():
            if (not i.startswith('_') and not callable(getattr(self, i))):
                if(i != 'jid' and i != 'j_timestamp'):
                    if (getattr(self, i) != getattr(obj, i)):
                        return False
        return True

    def jsci_payload(self):
        """
        Returns all data fields and values of jaseci object as json string.
        This grabs any fields that are added into inherited objects. Useful for
        saving and loading item.
        """
        obj_fields = []
        element_fields = dir(element(h=mem_hook()))
        for i in vars(self).keys():
            if not i.startswith('_') and i not in element_fields:
                obj_fields.append(i)
        obj_dict = {}
        for i in obj_fields:
            obj_dict[i] = getattr(self, i)
        return json.dumps(obj_dict)

    def serialize(self, deep=0):
        """
        Serialize Jaseci object
        """
        jdict = {}
        for i in vars(self).keys():
            if not i.startswith('_'):
                jdict[i] = copy.copy(vars(self)[i])
                if (deep > 0 and isinstance(jdict[i], id_list)):
                    for j in range(len(jdict[i])):
                        jdict[i][j] = copy.copy(self._h.get_obj(uuid.UUID(
                            jdict[i][j])).serialize(deep - 1))
        return jdict

    def json(self, deep=0):
        """
        Returns entire self object as Json string

        deep indicates number of levels to unwind uuids
        """
        return json.dumps(self.serialize(deep), indent=4)

    def json_load(self, blob):
        """Loads self from json blob"""
        jdict = json_str_to_jsci_dict(blob, owner_obj=self)
        for i in jdict.keys():
            setattr(self, i, jdict[i])

    def __str__(self):
        """
        String representation is of the form type:name:kind
        """
        return self.j_type + ':' + self.kind + ':' + self.name + \
            ':' + self.jid

    def __repr__(self):
        return self.__str__()
