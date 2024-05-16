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
    edge_ids: list[UUID] = []
    persistent: bool = False

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state.pop("obj")
        if self.edges:
            edges = state.pop("edges")
            state["edge_ids"] = [e._jac_.id for e in edges]

        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self.edge_ids = state.pop("edge_ids")

    def populate_edges(self) -> None:
        if len(self.edges) == 0 and len(self.edge_ids) > 0:
            for e_id in self.edge_ids:
                edge = Jac.context().get_obj(e_id)
                self.edges.append(edge)
            self.edge_ids.clear()

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
        self._jac_.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_jac_"] = self._jac_.__getstate__()
        return state

    def __setstate__(self, state):
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
        self.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_jac_"] = self._jac_.__getstate__()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._jac_ = PersistentEdgeAnchor(obj=self)
        self._jac_.__setstate__(state["_jac_"])

    def populate_nodes(self):
        if self._jac_.source_id:
            self._jac_.source = Jac.context().get_obj(self._jac_.source_id)
            self._jac_.source_id = None
        if self._jac_.target_id:
            self._jac_.target = Jac.context().get_obj(self._jac_.target_id)
            self._jac_.target_id = None


class PersistentGenericEdge(GenericEdge, PersistentEdgeArchitype):
    pass


class PersistentRoot(Root, PersistentNodeArchitype):
    """Root architype override"""

    def __init__(self):
        PersistentNodeArchitype.__init__(self)
        self._jac_.id = "root"
        self._jac_.persistent = True

    def __getstate__(self):
        return PersistentNodeArchitype.__getstate__(self)

    def __setstate__(self, state):
        return PersistentNodeArchitype.__setstate__(self, state)
