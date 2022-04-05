"""
Jaseci object mixins

Various mixins to define properties of Jaseci objects
"""
from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger
import uuid


class anchored():
    """Utility class for objects that hold anchor values"""

    def __init__(self):
        self.anchor = None

    def anchor_value(self):
        """Returns value of anchor context object"""
        if(self.anchor):
            return self.context[self.anchor]
        return None


class sharable():
    """Utility class for objects that are sharable between users"""

    def __init__(self, m_id, mode='private'):
        self.set_master(m_id)
        self.j_access = mode
        self.j_r_acc_ids = id_list(self)
        self.j_rw_acc_ids = id_list(self)

    @property
    def _m_id(self) -> str:
        return self.j_master

    def set_master(self, m_id):
        if(m_id is None or m_id == 'anon'):
            m_id = uuid.UUID(int=0).urn
        self.j_master = m_id

    def make_public(self):
        """Make element publically accessible"""
        self.j_access = 'public'
        self.save()

    def make_read_only(self):
        """Make element publically readable"""
        self.j_access = 'read_only'
        self.save()

    def make_private(self):
        """Make element private"""
        self.j_access = 'private'
        self.save()

    def is_public(self):
        """Check if element is publically accessible"""
        return self.j_access == 'public' or \
            self.j_master == uuid.UUID(int=0).urn

    def is_read_only(self):
        """Check if element is publically readable"""
        return self.j_access == 'read_only'

    def is_readable(self):
        """Check if element is publically readable"""
        return self.j_access == 'read_only' or self.is_public()

    def is_private(self):
        """Check if element is private"""
        return self.j_access == 'private'

    def super_check(self, caller_id):
        """Quick check if caller is super master"""
        if(not hasattr(self, "_h")):
            return False
        user = self._h.get_obj(caller_id, uuid.UUID(caller_id), override=True)
        if(user.j_type == 'super_master'):
            return True
        return False

    def check_read_access(self, caller_id, silent=False):
        if(caller_id == self._m_id or self.is_readable() or
           caller_id in self.j_r_acc_ids or
           caller_id in self.j_rw_acc_ids or
           self.super_check(caller_id)):
            return True
        if(not silent):
            logger.error(str(
                f'{caller_id} does not have permission to access {self}'))
        return False

    def check_write_access(self, caller_id, silent=False):
        if(caller_id == self._m_id or self.is_public() or
           caller_id in self.j_rw_acc_ids or
           self.super_check(caller_id)):
            return True
        if(not silent):
            logger.error(str(
                f'{caller_id} does not have permission to access {self}'))
        return False

    def give_access(self, m, read_only=True):
        """Give access to a master (user)"""
        if(not m.is_master()):
            logger.error(f'{m} is not master!')
            return False
        if(read_only and m.jid not in self.j_r_acc_ids):
            self.j_r_acc_ids.add_obj(m)
        elif(m.jid not in self.j_rw_acc_ids):
            self.j_rw_acc_ids.add_obj(m)
        return True

    def remove_access(self, m):
        """Remove access from a master (user)"""
        ret = False
        if(m.jid in self.j_r_acc_ids):
            self.j_r_acc_ids.remove_obj(m)
            ret = True
        if(m.jid in self.j_rw_acc_ids):
            self.j_rw_acc_ids.remove_obj(m)
            ret = True
        return ret


class hookable(sharable):
    """Utility class for objects that are savable to DBs and other stores"""

    def __init__(self, h, m_id, persist: bool = True, *args, **kwargs):
        self._h = h  # hook for storing and loading to persistent store
        self._persist = persist
        sharable.__init__(self, m_id, *args, **kwargs)

    def check_hooks_match(self, target, silent=False):
        """Checks whether target object hook matches self's hook"""
        if(not silent and target._h != self._h):
            logger.critical(str("Hook for {} does not match {}, {} != {}".
                                format(target, self, target._h, self._h)))
        return target._h == self._h

    def save(self):
        """
        Write self through hook to persistent storage
        """
        self._h.save_obj(self._m_id, self, self._persist)

    def destroy(self):
        """
        Destroys self from persistent storage

        Note that the object will still exist in python until GC'd
        """
        self._h.destroy_obj(self._m_id, self, self._persist)
        del self

    def parent(self):
        """
        Returns the objects for list of owners of this element
        """
        return self._h.get_obj(self._m_id, self.parent_id)
