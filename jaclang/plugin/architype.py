"""
Architypes override
"""

from jaclang.core.construct import NodeArchitype, EdgeArchitype, Root, GenericEdge
from jaclang.plugin.feature import JacFeature as Jac

from uuid import uuid4


class PersistentNodeArchitype(NodeArchitype):
    """Node architype override"""

    persistent: bool = False

    def __init__(self):
        super().__init__()
        Jac.memory_hook().save_obj(self, persistent=self.persistent)

    def save(self):
        self.persistent = True
        Jac.memory_hook().save_obj(self, persistent=True)


class PersistentEdgeArchitype(EdgeArchitype):
    """Edge architype override"""

    persistent: bool = False

    def __init__(self):
        super().__init__()
        Jac.memory_hook().save_obj(self, persistent=self.persistent)

    def save(self):
        self.persistent = True
        Jac.memory_hook().save_obj(self, persistent=True)


class PersistentGenericEdge(GenericEdge, PersistentEdgeArchitype):
    pass


class PersistentRoot(Root, PersistentNodeArchitype):
    """Root architype override"""

    persistent: bool = True

    @classmethod
    def make_root(cls):
        root = Jac.memory_hook().get_obj("root")
        if root is None:
            root = cls()

        return root

    def __init__(self):
        # check if a root node already exist
        # This should probably be part of a user/master object instead of a special key
        Root.__init__(self)
        self._jac_.id = "root"
        Jac.memory_hook().save_obj(self, persistent=self.persistent)
