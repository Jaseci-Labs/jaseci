"""Memory abstraction for jaseci plugin."""

from dataclasses import dataclass
from os import getenv
from typing import Callable, Generator, Iterable, TypeVar, cast

from bson import ObjectId

from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.memory import Memory


from pymongo import InsertOne
from pymongo.client_session import ClientSession

from .architype import (
    Anchor,
    BaseAnchor,
    BulkWrite,
    EdgeAnchor,
    NodeAnchor,
    Root,
    WalkerAnchor,
)
from ..jaseci.datasources import Collection

DISABLE_AUTO_CLEANUP = getenv("DISABLE_AUTO_CLEANUP") == "true"
SINGLE_QUERY = getenv("SINGLE_QUERY") == "true"
IDS = ObjectId | Iterable[ObjectId]
BA = TypeVar("BA", bound="BaseAnchor")


@dataclass
class MongoDB(Memory[ObjectId, BaseAnchor | Anchor]):
    """Shelf Handler."""

    __session__: ClientSession | None = None

    def populate_data(self, edges: Iterable[EdgeAnchor]) -> None:
        """Populate data to avoid multiple query."""
        if not SINGLE_QUERY:
            nodes: set[NodeAnchor] = set()
            for edge in self.find(edges):
                if edge.source:
                    nodes.add(edge.source)
                if edge.target:
                    nodes.add(edge.target)
            self.find(nodes)

    def find(  # type: ignore[override]
        self,
        anchors: BA | Iterable[BA],
        filter: Callable[[Anchor], Anchor] | None = None,
        session: ClientSession | None = None,
    ) -> Generator[BA, None, None]:
        """Find anchors from datasource by ids with filter."""
        if not isinstance(anchors, Iterable):
            anchors = [anchors]

        collections: dict[type[Collection[BaseAnchor]], list[ObjectId]] = {}
        for anchor in anchors:
            if anchor.id not in self.__mem__ and anchor not in self.__gc__:
                coll = collections.get(anchor.Collection)
                if coll is None:
                    coll = collections[anchor.Collection] = []

                coll.append(anchor.id)

        for cl, ids in collections.items():
            for anch_db in cl.find(
                {
                    "_id": {"$in": ids},
                },
                session=session or self.__session__,
            ):
                self.__mem__[anch_db.id] = anch_db

        for anchor in anchors:
            if (
                anchor not in self.__gc__
                and (anch_mem := self.__mem__.get(anchor.id))
                and (not filter or filter(anch_mem))  # type: ignore[arg-type]
            ):
                yield cast(BA, anch_mem)

    def find_one(  # type: ignore[override]
        self,
        anchors: BA | Iterable[BA],
        filter: Callable[[Anchor], Anchor] | None = None,
        session: ClientSession | None = None,
    ) -> BA | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(anchors, filter, session), None)

    def find_by_id(self, anchor: BA) -> BA | None:
        """Find one by id."""
        data = super().find_by_id(anchor.id)

        if not data and (data := anchor.Collection.find_by_id(anchor.id)):
            self.__mem__[data.id] = data

        return data

    def close(self) -> None:
        """Close memory handler."""
        bulk_write = self.get_bulk_write()

        if bulk_write.has_operations:
            if session := self.__session__:
                bulk_write.execute(session)
            else:
                with Collection.get_session() as session, session.start_transaction():
                    bulk_write.execute(session)

        super().close()

    def get_bulk_write(self) -> BulkWrite:
        """Sync memory to database."""
        bulk_write = BulkWrite()

        for anchor in self.__gc__:
            match anchor:
                case NodeAnchor():
                    bulk_write.del_node(anchor.id)
                case EdgeAnchor():
                    bulk_write.del_edge(anchor.id)
                case WalkerAnchor():
                    bulk_write.del_walker(anchor.id)
                case _:
                    pass

        for anchor in self.__mem__.values():
            if anchor.architype and anchor.persistent:
                if not anchor.state.connected:
                    anchor.state.connected = True
                    anchor.sync_hash()
                    bulk_write.operations[anchor.__class__].append(
                        InsertOne(anchor.serialize())
                    )
                elif (new_hash := anchor.has_changed()) and Jac.check_connect_access(
                    anchor  # type: ignore[arg-type]
                ):
                    anchor.state.full_hash = new_hash
                    if (
                        not DISABLE_AUTO_CLEANUP
                        and isinstance(anchor, NodeAnchor)
                        and not isinstance(anchor.architype, Root)
                        and not anchor.edges
                    ):
                        bulk_write.del_node(anchor.id)
                    else:
                        anchor.update(bulk_write)

        return bulk_write
