"""
Base Jaseci object class

Naming conventions
* '_ids', '_id' - appended to lists of ids as feilds of jaseci objects
* 'obj' - used to represent a jaseci object
* 'item' - Items are kv pairs derived from item class, dont use elsewhere
* 'store' - refers to persistent store for hooks from engine, (dont use db)
"""

import copy
import json
import uuid
from datetime import datetime

from jaseci.prim.obj_mixins import Hookable
from jaseci.jsorc.memory import MemoryHook
from jaseci.utils.id_list import IdList
from jaseci.utils.json_handler import JaseciJsonEncoder, json_str_to_jsci_dict
from jaseci.utils.utils import log_var_out, logger, camel_to_snake

__version__ = "1.0.0"
element_fields = None


class Element(Hookable):
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

    def __init__(
        self,
        name="basic",
        kind="generic",
        auto_save=True,
        **kwargs,
    ):
        self.name = name
        self.kind = kind
        self.jid = uuid.uuid4().urn
        self.j_timestamp = datetime.utcnow().isoformat()
        self.j_type = camel_to_snake(type(self).__name__)
        Hookable.__init__(self, **kwargs)
        if self.is_master():
            self.set_master(self.jid)
        if auto_save:
            self.save()

    @property
    def id(self):
        return uuid.UUID(self.jid)

    @id.setter
    def id(self, obj):
        self.jid = obj.urn

    @property
    def timestamp(self):
        return datetime.fromisoformat(self.j_timestamp)

    @timestamp.setter
    def timestamp(self, obj):
        self.j_timestamp = obj.isoformat()

    def is_master(self, super_check=False, silent=True):
        """Check if self is a master"""
        ret = True
        if "master" not in self.j_type:
            ret = False
            if not silent:
                logger.error(f"{self} is not master")
        if super_check and "super" not in self.j_type:
            ret = False
            if not silent:
                logger.error(f"{self} does not have super master status")
        return ret

    def get_master(self):
        """Get the master of an element"""
        return self._h.get_obj(self._m_id, self.j_master)

    def duplicate(self, persist_dup: bool = False):
        """
        Duplicates elements by creating copy with new id
        Hook override to duplicate into mem / another store
        """
        kwargs = {"m_id": self._m_id, "h": self._h, "persist": persist_dup}
        dup = type(self)(**kwargs)
        id_save = dup.id
        for i in dup.__dict__.keys():
            if type(dup.__dict__[i]) == IdList:
                setattr(dup, i, IdList(parent_obj=dup, in_list=self.__dict__[i]))
            else:
                setattr(dup, i, self.__dict__[i])
        dup.id = id_save
        dup.timestamp = datetime.utcnow()
        dup.save()
        return dup

    def is_equivalent(self, obj):
        """
        Duplicates elements by creating copy with new id
        """
        if self.j_type != obj.j_type:
            return False
        for i in vars(self).keys():
            if not i.startswith("_") and not callable(getattr(self, i)):
                if i != "jid" and i != "j_timestamp":
                    if getattr(self, i) != getattr(obj, i):
                        return False
        return True

    def jsci_payload(self):
        """
        Returns all data fields and values of jaseci object as json string.
        This grabs any fields that are added into inherited objects. Useful for
        saving and loading item.
        """
        global element_fields
        if element_fields is None:
            element_fields = dir(Element(m_id=0, h=MemoryHook()))
        obj_fields = []
        for i in vars(self).keys():
            if not i.startswith("_") and i not in element_fields:
                obj_fields.append(i)
        obj_dict = {}
        for i in obj_fields:
            obj_dict[i] = getattr(self, i)
        return json.dumps(obj_dict, cls=JaseciJsonEncoder)

    def serialize(self, deep=0, detailed=False):
        """
        Serialize Jaseci object
        """
        jdict = {}
        key_fields = [
            "name",
            "kind",
            "jid",
            "j_type",
            "context",
            "code_sig",
            "j_timestamp",
            "version",
            "to_node_id",
            "from_node_id",
        ]
        for i in vars(self).keys():
            if not i.startswith("_"):
                if not detailed and i not in key_fields:
                    continue
                jdict[i] = copy.copy(vars(self)[i])
                if not detailed and i == "context":
                    for j in self.private_values():
                        del jdict[i][j]
                if deep > 0 and isinstance(jdict[i], IdList):
                    for j in range(len(jdict[i])):
                        jdict[i][j] = copy.copy(
                            self._h.get_obj(self._m_id, jdict[i][j]).serialize(deep - 1)
                        )
        return jdict

    def json(self, deep=0, detailed=False):
        """
        Returns entire self object as Json string

        deep indicates number of levels to unwind uuids
        """
        return json.dumps(
            self.serialize(deep, detailed=detailed), indent=4, cls=JaseciJsonEncoder
        )

    def json_load(self, blob):
        """Loads self from json blob"""
        jdict = json_str_to_jsci_dict(blob, parent_obj=self)
        self.dict_load(jdict=jdict)

    def dict_load(self, jdict):
        """Loads self from dict"""
        for i in jdict.keys():
            if i in vars(self).keys():
                setattr(self, i, jdict[i])

    def get_deep_obj_list(self, objs=None):
        """Recursively get all contained Jaseci objects and return id_list"""
        if objs is None:
            objs = []
        objs.append(self)
        for i in self.__dict__.keys():
            if str(i).endswith("_ids") and isinstance(self.__dict__[i], IdList):
                for j in self.__dict__[i].obj_list():
                    if j not in objs:
                        j.get_deep_obj_list(objs=objs)
        return objs

    def propagate_access(self, set_access=None):
        """Propagate permission through id_lists hierarchy"""
        if set_access is None:
            set_access = self.j_access
        for i in self.get_deep_obj_list():
            i.j_access = set_access

    def log_output(self, val):
        """
        Utility to log out variable in pretty format
        """
        log_var_out(val)

    def __str__(self):
        """
        String representation is of the form type:name:kind
        """
        return self.j_type + ":" + self.kind + ":" + self.name + ":" + self.jid

    def __repr__(self):
        return self.__str__()
