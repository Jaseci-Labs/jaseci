"""Memory abstraction for jaseci plugin."""

from dataclasses import dataclass, field
from os import getenv
from typing import Callable, Generator, Iterable, TypeVar

from bson import ObjectId

from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.memory import Memory


from pymongo import InsertOne
from pymongo.client_session import ClientSession

from .architype import (
    BulkWrite,
    EdgeAnchor,
    JacCloudJID,
    NodeAnchor,
    ObjectAnchor,
    Root,
    WalkerAnchor,
)
from ..jaseci.datasources import Collection

DISABLE_AUTO_CLEANUP = getenv("DISABLE_AUTO_CLEANUP") == "true"
SINGLE_QUERY = getenv("SINGLE_QUERY") == "true"

_ANCHOR = TypeVar("_ANCHOR", NodeAnchor, EdgeAnchor, WalkerAnchor, ObjectAnchor)


@dataclass
class MongoDB(Memory):
    """Shelf Handler."""

    __mem__: dict[
        JacCloudJID, NodeAnchor | EdgeAnchor | WalkerAnchor | ObjectAnchor
    ] = field(
        default_factory=dict
    )  # type: ignore[assignment]
    __gc__: set[JacCloudJID] = field(default_factory=set)  # type: ignore[assignment]
    __session__: ClientSession | None = None

    def populate_data(self, edges: Iterable[JacCloudJID[EdgeAnchor]]) -> None:
        """Populate data to avoid multiple query."""
        if not SINGLE_QUERY:
            nodes: set[JacCloudJID] = set()
            for edge in self.find(edges):
                nodes.add(edge.source)
                nodes.add(edge.target)
            self.find(nodes)

    def find(  # type: ignore[override]
        self,
        ids: JacCloudJID[_ANCHOR] | Iterable[JacCloudJID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
        session: ClientSession | None = None,
    ) -> Generator[_ANCHOR, None, None]:
        """Find anchors from datasource by ids with filter."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        collections: dict[
            type[
                Collection[NodeAnchor]
                | Collection[EdgeAnchor]
                | Collection[WalkerAnchor]
                | Collection[ObjectAnchor]
            ],
            list[ObjectId],
        ] = {}
        for jid in ids:
            if jid not in self.__mem__ and jid not in self.__gc__:
                coll = collections.get(jid.type.Collection)
                if coll is None:
                    coll = collections[jid.type.Collection] = []

                coll.append(jid.id)

        for cl, oids in collections.items():
            for anch_db in cl.find(
                {
                    "_id": {"$in": oids},
                },
                session=session or self.__session__,
            ):
                self.__mem__[anch_db.jid] = anch_db

        for jid in ids:
            if (
                jid not in self.__gc__
                and (anch_mem := self.__mem__.get(jid))
                and isinstance(anch_mem, jid.type)
                and (not filter or filter(anch_mem))
            ):
                yield anch_mem

    def find_one(  # type: ignore[override]
        self,
        ids: JacCloudJID[_ANCHOR] | Iterable[JacCloudJID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
        session: ClientSession | None = None,
    ) -> _ANCHOR | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter, session), None)

    def find_by_id(self, id: JacCloudJID[_ANCHOR]) -> _ANCHOR | None:  # type: ignore[override]
        """Find one by id."""
        data = super().find_by_id(id)

        if not data and (data := id.type.Collection.find_by_id(id.id)):
            self.__mem__[data.jid] = data

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

    def sync_mem_to_db(
        self, bulk_write: BulkWrite, keys: Iterable[JacCloudJID]
    ) -> None:
        """Manually sync memory to db."""
        for key in keys:
            if (
                (anchor := self.__mem__.get(key))
                and anchor.architype
                and anchor.persistent
            ):
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

    def get_bulk_write(self) -> BulkWrite:
        """Sync memory to database."""
        bulk_write = BulkWrite()
        for jid in self.__gc__:
            self.__mem__.pop(jid, None)
            # match case doesn't work yet with
            # type checking for type (not instance)
            if jid.type is NodeAnchor:
                bulk_write.del_node(jid.id)
            elif jid.type is EdgeAnchor:
                bulk_write.del_edge(jid.id)
            elif jid.type is WalkerAnchor:
                bulk_write.del_walker(jid.id)
            elif jid.type is ObjectAnchor:
                bulk_write.del_object(jid.id)

        keys = set(self.__mem__.keys())

        # current memory
        self.sync_mem_to_db(bulk_write, keys)

        # additional after memory sync
        self.sync_mem_to_db(bulk_write, set(self.__mem__.keys() - keys))

        return bulk_write
