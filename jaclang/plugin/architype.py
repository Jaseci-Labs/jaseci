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


class PersistentRoot(Root, PersistentNodeArchitype):
    """Root architype override"""

    def __init__(self):
        # check if a root node already exist
        # This should probably be part of a user/master object instead of a special key
        print("I am in PersistentRoot")
        root = Storage.get_obj("root")
        if root is None:
            print("calling root init")
            NodeArchitype.__init__(self)
            Root.__init__(self)
            self._jac_.id = "root"
            self._test_id_ = uuid4()
            print("setting root test id to be", self._test_id_)
            Storage.save_obj(self)
        else:
            self = root
            print("root already exists")
            print(self._test_id_)
            print("root already exists")
