"""
Architypes override
"""

from jaclang.core.construct import (
    NodeArchitype,
    EdgeArchitype,
    Root,
    GenericEdge,
    NodeAnchor,
    EdgeAnchor,
)
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.compiler.constant import EdgeDir

from uuid import uuid4, UUID
from typing import Any, Optional, Callable


class PersistentNodeAnchor(NodeAnchor):
    edges_id: list[UUID] = []
    persistent: bool = False

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state.pop("obj")
        edges = state.pop("edges")
        state["edges_id"] = [e._jac_.id for e in edges]
        print("PersistentNodeAnchor.__getstate__", self, state)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        print("PersistentNodeAnchor.__setstate__", self, state)
        self.__dict__.update(state)
        self.edges_id = state.pop("edges_id")

    def populate_edges(self) -> None:
        print("PersistentNodeAnchor.populate_edges", self, self.edges, self.edges_id)
        if len(self.edges) == 0 and len(self.edges_id) > 0:
            for e_id in self.edges_id:
                edge = Jac.context().get_obj(e_id)
                self.edges.append(edge)

    def get_edges(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        self.populate_edges()
        return super().get_edges(dir, filter_func, target_obj)

    def edges_to_nodes(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        self.populate_edges()
        return super().edges_to_nodes(dir, filter_func, target_obj)


class PersistentEdgeAnchor(EdgeAnchor):
    persistent: bool = False
    source_id: Optional[UUID] = None
    target_id: Optional[UUID] = None

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state.pop("obj")

        if self.source:
            state["source_id"] = self.source._jac_.id

        if self.target:
            state["target_id"] = self.target._jac_.id

        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)


class PersistentNodeArchitype(NodeArchitype):
    """Node architype override"""

    def __init__(self):
        self._jac_ = PersistentNodeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self._jac_.persistent)

    def save(self):
        print("PersistentNodeArchitype.save", self)
        self._jac_.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        print(type(self._jac_))
        state["_jac_"] = self._jac_.__getstate__()
        print("PersistentNodeArchitype.__getstate__", self, state)
        return state

    def __setstate__(self, state):
        print("PersistentNodeArchitype.__setstate__", state)
        self.__dict__.update(state)
        self._jac_ = PersistentNodeAnchor(obj=self)
        self._jac_.__setstate__(state["_jac_"])


class PersistentEdgeArchitype(EdgeArchitype):
    """Edge architype override"""

    persistent: bool = False

    def __init__(self) -> None:
        self._jac_ = PersistentEdgeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self.persistent)

    def save(self):
        print("PersistentEdgeArchitype.save", self)
        self.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_jac_"] = self._jac_.__getstate__()
        print("PersistentEdgeArchitype.__getstate__", self, state)
        return state

    def __setstate__(self, state):
        print("PersistentEdgeArchitype.__setstate__", self, state)
        self.__dict__.update(state)
        self._jac_ = PersistentEdgeAnchor(obj=self)
        self._jac_.__setstate__(state["_jac_"])

    def populate_nodes(self):
        if self._jac_.source_id:
            self._jac_.source = Jac.context().get_obj(self._jac_.source_id)
        if self._jac_.target_id:
            self._jac_.target = Jac.context().get_obj(self._jac_.target_id)


class PersistentGenericEdge(GenericEdge, PersistentEdgeArchitype):
    pass


class PersistentRoot(Root, PersistentNodeArchitype):
    """Root architype override"""

    #  @classmethod
    #  def make_root(cls):
    #      root = Jac.context().get("root")
    #      if root is None:
    #          root = cls()

    #      return root

    def __init__(self):
        # check if a root node already exist
        # This should probably be part of a user/master object instead of a special key
        PersistentNodeArchitype.__init__(self)
        self._jac_.id = "root"
        self._jac_.persistent = True
        # Jac.context().set(self, persistent=self.persistent)

    def __getstate__(self):
        return PersistentNodeArchitype.__getstate__(self)

    def __setstate__(self, state):
        return PersistentNodeArchitype.__setstate__(self, state)
