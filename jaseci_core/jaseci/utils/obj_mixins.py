"""
Jaseci object mixins

Various mixins to define properties of Jaseci objects
"""
from jaseci.utils.mem_hook import mem_hook


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
