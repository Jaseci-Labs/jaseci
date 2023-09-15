"""
Jaseci object mixins

Various mixins to define properties of Jaseci objects
"""
from jaseci.utils.id_list import IdList
from jaseci.utils.utils import logger
import uuid


class Anchored:
    """Utility class for objects that hold anchor values"""

    arch_map = {}

    def __init__(self):
        self.context = {}

    def get_architype(self):
        arch = self.get_arch_from_cache()  # Optimization
        if arch and id(arch._h) == id(self._h):
            return arch
        arch = (
            self._h._machine.parent().get_arch_for(self)
            if self._h._machine is not None
            and self._h._machine.parent() is not None
            and self._h._machine.parent().j_type == "sentinel"
            else None
        )
        mast = self.get_master()
        if arch is None and mast.active_snt() is not None:
            arch = mast.active_snt().get_arch_for(self)
        elif arch is None and self.parent() and self.parent().j_type == "sentinel":
            arch = self.parent().get_arch_for(self)
        self.cache_arch(arch)
        return arch

    def cache_arch(self, arch):
        Anchored.arch_map[self.kind + self.name] = arch

    def get_arch_from_cache(self):
        if (self.kind + self.name) in Anchored.arch_map:
            return Anchored.arch_map[self.kind + self.name]
        return None

    def flush_cache():
        Anchored.arch_map = {}

    def anchor_value(self):
        """Returns value of anchor context object"""
        arch = self.get_architype()
        if arch is not None:
            anch = arch.anchor_var
            if anch and anch in self.context.keys():
                return self.context[anch]
        return None

    def private_values(self):
        """Returns value of anchor context object"""
        arch = self.get_architype()
        if arch is not None:
            return arch.private_vars
        return []

    def set_context(self, ctx):
        """Assign values to context fields of object"""
        for i in ctx.keys():
            if i in self.get_architype().has_vars:
                self.context[i] = ctx[i]
            else:
                logger.warning(str(f"{i} not a context member of {self}"))
        self.save()


class Sharable:
    """Utility class for objects that are sharable between users"""

    def __init__(self, m_id, mode=None, **kwargs):
        self.set_master(m_id)
        self.j_access = (
            mode
            if mode is not None
            else self._h.get_obj(self._m_id, self._m_id).perm_default
            if self._h.has_obj(self._m_id)
            else "private"
        )
        self.j_r_acc_ids = IdList(self)
        self.j_rw_acc_ids = IdList(self)

    @property
    def _m_id(self) -> str:
        return self.j_master

    def set_master(self, m_id):
        if not m_id:
            m_id = uuid.UUID(int=0).urn
        self.j_master = m_id

    def make_public(self):
        """Make element publically accessible"""
        self.j_access = "public"
        self.save()

    def make_read_only(self):
        """Make element publically readable"""
        self.j_access = "read_only"
        self.save()

    def make_private(self):
        """Make element private"""
        self.j_access = "private"
        self.save()

    def is_public(self):
        """Check if element is publically accessible"""
        return self.j_access == "public" or self.j_master == uuid.UUID(int=0).urn

    def is_read_only(self):
        """Check if element is publically readable"""
        return self.j_access == "read_only"

    def is_readable(self):
        """Check if element is publically readable"""
        return self.j_access == "read_only" or self.is_public()

    def is_private(self):
        """Check if element is private"""
        return self.j_access == "private"

    def super_check(self, caller_id):
        """Quick check if caller is super master"""
        if not hasattr(self, "_h"):
            return False
        user = self._h.get_obj(caller_id, caller_id, override=True)
        if user.j_type == "super_master":
            return True
        return False

    def check_read_access(self, caller_id, silent=False):
        if (
            caller_id == self._m_id
            or self.is_readable()
            or caller_id in self.j_r_acc_ids
            or caller_id in self.j_rw_acc_ids
            or self.super_check(caller_id)
        ):
            return True
        if not silent:
            logger.error(str(f"{caller_id} does not have permission to access {self}"))
        return False

    def check_write_access(self, caller_id, silent=False):
        if (
            caller_id == self._m_id
            or self.is_public()
            or caller_id in self.j_rw_acc_ids
            or self.super_check(caller_id)
        ):
            return True
        if not silent:
            logger.error(str(f"{caller_id} does not have permission to access {self}"))
        return False

    def give_access(self, m, read_only=True):
        """Give access to a master (user)"""
        if not m.is_master():
            logger.error(f"{m} is not master!")
            return False
        if read_only and m.jid not in self.j_r_acc_ids:
            self.j_r_acc_ids.add_obj(m)
        elif m.jid not in self.j_rw_acc_ids:
            self.j_rw_acc_ids.add_obj(m)
        return True

    def remove_access(self, m):
        """Remove access from a master (user)"""
        ret = False
        if m.jid in self.j_r_acc_ids:
            self.j_r_acc_ids.remove_obj(m)
            ret = True
        if m.jid in self.j_rw_acc_ids:
            self.j_rw_acc_ids.remove_obj(m)
            ret = True
        return ret


class Hookable(Sharable):
    """Utility class for objects that are savable to DBs and other stores"""

    def __init__(self, h, persist: bool = True, parent=None, **kwargs):
        self._h = h  # hook for storing and loading to persistent store
        self._persist = persist
        self.j_parent = parent.jid if parent else None  # member of
        Sharable.__init__(self, **kwargs)

    def check_hooks_match(self, target, silent=False):
        """Checks whether target object hook matches self's hook"""
        if not self._m_id or not target._m_id:
            return True
        elif not silent and target._h != self._h:
            logger.critical(
                str(
                    "Hook for {} does not match {}, {} != {}".format(
                        target, self, target._h, self._h
                    )
                )
            )
        return target._h == self._h

    def make_persistent(self):
        """Make element persistent"""
        self._persist = True
        self.save()

    def save(self):
        """
        Write self through hook to persistent storage
        """
        self._h.save_obj(self._m_id, self)

    def destroy(self):
        """
        Destroys self from persistent storage

        Note that the object will still exist in python until GC'd
        """
        self._h.destroy_obj(self._m_id, self)
        del self

    def parent(self):
        """
        Returns the objects for list of owners of this element
        """
        if self.j_parent:
            return self._h.get_obj(self._m_id, self.j_parent)
