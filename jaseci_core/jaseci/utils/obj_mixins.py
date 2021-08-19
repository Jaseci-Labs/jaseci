"""
Jaseci object mixins

Various mixins to define properties of Jaseci objects
"""
from jaseci.utils.mem_hook import mem_hook
from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger


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

    def __init__(self, m, mode='private'):
        self.j_master = m
        self._m = self.j_master
        self.j_mode = mode
        self.j_r_acc_ids = []  # id_list(self)
        self.j_rw_acc_ids = []  # id_list(self)

    def make_public(self):
        """Make element publically accessible"""
        self.j_mode = 'public'

    def make_private(self):
        """Make element private"""
        self.j_mode = 'private'

    def give_access(self, m, read_only=True):
        """Give access to a master (user)"""
        if(m.j_type != 'master'):
            logger.error(f'{m} is not master!')
            return False
        if(read_only):
            self.j_r_acc_ids.add_obj(m)
        else:
            self.j_rw_acc_ids.add_obj(m)
        return True

    def remove_access(self, m):
        """Remove access from a master (user)"""
        if(m.jid in self.j_r_acc_ids):
            self.j_r_acc_ids.remove_obj(m)
            return True
        if(m.jid in self.j_rw_acc_ids):
            self.j_rw_acc_ids.remove_obj(m)
            return True
        return False


class hookable():
    """Utility class for objects that are savable to DBs and other stores"""

    def __init__(self, h, persist: bool = True, *args, **kwargs):
        self._h = h  # hook for storing and loading to persistent store
        self._persist = persist
        #sharable.__init__(self, m,  *args, **kwargs)

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

    def parent(self):
        """
        Returns the objects for list of owners of this element
        """
        return self._h.get_obj(self.parent_id)
