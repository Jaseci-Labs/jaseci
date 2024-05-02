"""
Architypes override
"""

from jaclang.core.construct import NodeArchitype, Root, NodeAnchor
from jaclang.plugin.shelve_storage import Storage

from uuid import uuid4


class PersistentNodeArchitype(NodeArchitype):
    """Node architype override"""

    def __init__(self):
        super().__init__()
        print("I am in PersistentNodeArchitype")
        Storage.save_obj(self)


class PersistentRoot(Root):
    """Root architype override"""

    @classmethod
    def make_root(cls):
        print("I am in PersistentRoot")
        root = Storage.get_obj("root")
        if root is None:
            root = cls()

        return root

    def __init__(self):
        # check if a root node already exist
        # This should probably be part of a user/master object instead of a special key
        print("calling root init")
        Root.__init__(self)
        self._jac_.id = "root"
        Storage.save_obj(self)
