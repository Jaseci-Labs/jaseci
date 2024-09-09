"""Core constructs for Jac Language."""

from dataclasses import asdict as _asdict, dataclass, field, fields, is_dataclass
from enum import Enum
from os import getenv
from pickle import dumps as pdumps
from re import IGNORECASE, compile
from typing import (
    Any,
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    TypeVar,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from bson import ObjectId

from jaclang.compiler.constant import EdgeDir
from jaclang.runtimelib.architype import (
    Access as _Access,
    AccessLevel,
    Anchor,
    Architype,
    DSFunc,
    EdgeAnchor as _EdgeAnchor,
    EdgeArchitype as _EdgeArchitype,
    NodeAnchor as _NodeAnchor,
    NodeArchitype as _NodeArchitype,
    Permission as _Permission,
    TANCH,
    WalkerAnchor as _WalkerAnchor,
    WalkerArchitype as _WalkerArchitype,
)

from orjson import dumps

from pymongo import ASCENDING, DeleteMany, DeleteOne, InsertOne, UpdateMany, UpdateOne
from pymongo.client_session import ClientSession
from pymongo.errors import ConnectionFailure, OperationFailure

from ..jaseci.datasources import Collection as BaseCollection
from ..jaseci.utils import logger

MANUAL_SAVE = getenv("MANUAL_SAVE")
GENERIC_ID_REGEX = compile(r"^(n|e|w):([^:]*):([a-f\d]{24})$", IGNORECASE)
NODE_ID_REGEX = compile(r"^n:([^:]*):([a-f\d]{24})$", IGNORECASE)
EDGE_ID_REGEX = compile(r"^e:([^:]*):([a-f\d]{24})$", IGNORECASE)
WALKER_ID_REGEX = compile(r"^w:([^:]*):([a-f\d]{24})$", IGNORECASE)
T = TypeVar("T")
TBA = TypeVar("TBA", bound="BaseArchitype")


def asdict_factory(data: Iterable[tuple]) -> dict[str, Any]:
    """Parse dataclass to dict."""
    _data = {}
    for key, value in data:
        if isinstance(value, Enum):
            _data[key] = value.name
        else:
            _data[key] = value
    return _data


def asdict(obj: object) -> dict[str, Any]:
    """Override dataclass asdict."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return _asdict(obj, dict_factory=asdict_factory)
    raise ValueError("Object is not a dataclass!")


def architype_to_dataclass(cls: type[T], data: dict[str, Any], **kwargs: object) -> T:
    """Parse dict to architype."""
    _to_dataclass(cls, data)
    architype = object.__new__(cls)
    architype.__init__(**data, **kwargs)  # type: ignore[misc]
    return architype


def to_dataclass(cls: type[T], data: dict[str, Any], **kwargs: object) -> T:
    """Parse dict to dataclass."""
    _to_dataclass(cls, data)
    return cls(**data, **kwargs)


def _to_dataclass(cls: type[T], data: dict[str, Any]) -> None:
    """Parse dict to dataclass implementation."""
    hintings = get_type_hints(cls)
    if is_dataclass(cls):
        for attr in fields(cls):
            if target := data.get(attr.name):
                hint = hintings[attr.name]
                if is_dataclass(hint):
                    data[attr.name] = to_dataclass(hint, target)
                else:
                    origin = get_origin(hint)
                    if origin == dict and isinstance(target, dict):
                        if is_dataclass(inner_cls := get_args(hint)[-1]):
                            for key, value in target.items():
                                target[key] = to_dataclass(inner_cls, value)
                    elif (
                        origin == list
                        and isinstance(target, list)
                        and is_dataclass(inner_cls := get_args(hint)[-1])
                    ):
                        for key, value in enumerate(target):
                            target[key] = to_dataclass(inner_cls, value)
                    elif (
                        issubclass(hint, Enum)
                        and isinstance(target, str)
                        and (enum := hint.__members__.get(target))
                    ):
                        data[attr.name] = enum


@dataclass
class BulkWrite:
    """Bulk Write builder."""

    SESSION_MAX_TRANSACTION_RETRY: ClassVar[int] = int(
        getenv("SESSION_MAX_TRANSACTION_RETRY") or "1"
    )
    SESSION_MAX_COMMIT_RETRY: ClassVar[int] = int(
        getenv("SESSION_MAX_COMMIT_RETRY") or "1"
    )

    operations: dict[
        type["BaseAnchor"],
        list[InsertOne[Any] | DeleteMany | DeleteOne | UpdateMany | UpdateOne],
    ] = field(
        default_factory=lambda: {
            NodeAnchor: [],
            EdgeAnchor: [],
            WalkerAnchor: [],
        }
    )

    del_ops_nodes: list[ObjectId] = field(default_factory=list)
    del_ops_edges: list[ObjectId] = field(default_factory=list)
    del_ops_walker: list[ObjectId] = field(default_factory=list)

    def del_node(self, id: ObjectId) -> None:
        """Add node to delete many operations."""
        if not self.del_ops_nodes:
            self.operations[NodeAnchor].append(
                DeleteMany({"_id": {"$in": self.del_ops_nodes}})
            )

        self.del_ops_nodes.append(id)

    def del_edge(self, id: ObjectId) -> None:
        """Add edge to delete many operations."""
        if not self.del_ops_edges:
            self.operations[EdgeAnchor].append(
                DeleteMany({"_id": {"$in": self.del_ops_edges}})
            )

        self.del_ops_edges.append(id)

    def del_walker(self, id: ObjectId) -> None:
        """Add walker to delete many operations."""
        if not self.del_ops_walker:
            self.operations[WalkerAnchor].append(
                DeleteMany({"_id": {"$in": self.del_ops_walker}})
            )

        self.del_ops_walker.append(id)

    @property
    def has_operations(self) -> bool:
        """Check if has operations."""
        return any(val for val in self.operations.values())

    @staticmethod
    def commit(session: ClientSession) -> None:
        """Commit current session."""
        commit_retry = 0
        commit_max_retry = BulkWrite.SESSION_MAX_COMMIT_RETRY
        while commit_retry <= commit_max_retry:
            try:
                session.commit_transaction()
                break
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("UnknownTransactionCommitResult"):
                    commit_retry += 1
                    logger.error(
                        "Error commiting bulk write! "
                        f"Retrying [{commit_retry}/{commit_max_retry}] ..."
                    )
                    continue
                logger.error(
                    f"Error commiting bulk write after max retry [{commit_max_retry}] !"
                )
                raise
            except Exception:
                session.abort_transaction()
                logger.error("Error commiting bulk write!")
                raise

    def execute(self, session: ClientSession) -> None:
        """Execute all operations."""
        transaction_retry = 0
        transaction_max_retry = self.SESSION_MAX_TRANSACTION_RETRY
        while transaction_retry <= transaction_max_retry:
            try:
                if node_operation := self.operations[NodeAnchor]:
                    NodeAnchor.Collection.bulk_write(node_operation, False, session)
                if edge_operation := self.operations[EdgeAnchor]:
                    EdgeAnchor.Collection.bulk_write(edge_operation, False, session)
                if walker_operation := self.operations[WalkerAnchor]:
                    WalkerAnchor.Collection.bulk_write(walker_operation, False, session)
                self.commit(session)
                break
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("TransientTransactionError"):
                    transaction_retry += 1
                    logger.error(
                        "Error executing bulk write! "
                        f"Retrying [{transaction_retry}/{transaction_max_retry}] ..."
                    )
                    continue
                logger.error(
                    f"Error executing bulk write after max retry [{transaction_max_retry}] !"
                )
                raise
            except Exception:
                logger.error("Error executing bulk write!")
                raise


@dataclass
class Access(_Access):
    """Access Structure."""

    def serialize(self) -> dict[str, object]:
        """Serialize Access."""
        return {
            "anchors": {key: val.name for key, val in self.anchors.items()},
        }

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> "Access":
        """Deserialize Access."""
        anchors = cast(dict[str, str], data.get("anchors"))
        return Access(
            anchors={key: AccessLevel[val] for key, val in anchors.items()},
        )


@dataclass
class Permission(_Permission):
    """Anchor Access Handler."""

    roots: Access = field(default_factory=Access)

    def serialize(self) -> dict[str, object]:
        """Serialize Permission."""
        return {"all": self.all.name, "roots": self.roots.serialize()}

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> "Permission":
        """Deserialize Permission."""
        return Permission(
            all=AccessLevel[data.get("all", AccessLevel.NO_ACCESS.name)],
            roots=Access.deserialize(data.get("roots", {})),
        )


@dataclass
class AnchorState:
    """Anchor state handler."""

    changes: dict[str, dict[str, Any]] = field(default_factory=dict)
    full_hash: int = 0
    context_hashes: dict[str, int] = field(default_factory=dict)
    deleted: bool | None = None
    connected: bool = False


@dataclass(eq=False, repr=False, kw_only=True)
class BaseAnchor:
    """Base Anchor."""

    architype: "BaseArchitype"
    name: str = ""
    id: ObjectId = field(default_factory=ObjectId)
    root: ObjectId | None = None
    access: Permission
    state: AnchorState

    class Collection(BaseCollection["BaseAnchor"]):
        """Anchor collection interface."""

        pass

    @property
    def ref_id(self) -> str:
        """Return id in reference type."""
        return f"{self.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    @staticmethod
    def ref(ref_id: str) -> "BaseAnchor | Anchor":
        """Return ObjectAnchor instance if ."""
        if match := GENERIC_ID_REGEX.search(ref_id):
            cls: type[BaseAnchor]

            match match.group(1):
                case "n":
                    cls = NodeAnchor
                case "e":
                    cls = EdgeAnchor
                case "w":
                    cls = WalkerAnchor
                case _:
                    raise ValueError(f"{ref_id}] is not a valid reference!")
            anchor = object.__new__(cls)
            anchor.name = str(match.group(2))
            anchor.id = ObjectId(match.group(3))
            return anchor
        raise ValueError(f"{ref_id}] is not a valid reference!")

    ####################################################
    #                 QUERY OPERATIONS                 #
    ####################################################

    @property
    def _set(self) -> dict:
        if "$set" not in self.state.changes:
            self.state.changes["$set"] = {}
        return self.state.changes["$set"]

    @property
    def _unset(self) -> dict:
        if "$unset" not in self.state.changes:
            self.state.changes["$unset"] = {}
        return self.state.changes["$unset"]

    @property
    def _add_to_set(self) -> dict:
        if "$addToSet" not in self.state.changes:
            self.state.changes["$addToSet"] = {}

        return self.state.changes["$addToSet"]

    @property
    def _pull(self) -> dict:
        if "$pull" not in self.state.changes:
            self.state.changes["$pull"] = {}

        return self.state.changes["$pull"]

    def add_to_set(self, field: str, anchor: Anchor, remove: bool = False) -> None:
        """Add to set."""
        if field not in (add_to_set := self._add_to_set):
            add_to_set[field] = {"$each": set()}

        ops: set = add_to_set[field]["$each"]

        if remove:
            if anchor in ops:
                ops.remove(anchor)
        else:
            ops.add(anchor)
            self.pull(field, anchor, True)

    def pull(self, field: str, anchor: Anchor, remove: bool = False) -> None:
        """Pull from set."""
        if field not in (pull := self._pull):
            pull[field] = {"$in": set()}

        ops: set = pull[field]["$in"]

        if remove:
            if anchor in ops:
                ops.remove(anchor)
        else:
            ops.add(anchor)
            self.add_to_set(field, anchor, True)

    def connect_edge(self, anchor: Anchor) -> None:
        """Push update that there's newly added edge."""
        self.add_to_set("edges", anchor)

    def disconnect_edge(self, anchor: Anchor) -> None:
        """Push update that there's edge that has been removed."""
        self.pull("edges", anchor)

    def allow_root(
        self, root: "BaseAnchor", level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = self.access.roots
        if (ref_id := root.ref_id) and level != access.anchors.get(
            ref_id, AccessLevel.NO_ACCESS
        ):
            access.anchors[ref_id] = level
            self._set.update({f"access.roots.anchors.{ref_id}": level.name})
            self._unset.pop(f"access.roots.anchors.{ref_id}", None)

    def disallow_root(
        self, root: Anchor, level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = self.access.roots

        if (ref_id := root.ref_id) and access.anchors.pop(ref_id, None) is not None:
            self._unset.update({f"access.roots.anchors.{ref_id}": True})
            self._set.pop(f"access.roots.anchors.{ref_id}", None)

    def unrestrict(self, level: AccessLevel | int | str = AccessLevel.READ) -> None:
        """Allow everyone to access current Architype."""
        level = AccessLevel.cast(level)
        if level != self.access.all:
            self.access.all = level
            self._set.update({"access.all": level.name})

    def restrict(self) -> None:
        """Disallow others to access current Architype."""
        if self.access.all > AccessLevel.NO_ACCESS:
            self.access.all = AccessLevel.NO_ACCESS
            self._set.update({"access.all": AccessLevel.NO_ACCESS.name})

    ####################################################
    #                POPULATE OPERATIONS               #
    ####################################################

    def is_populated(self) -> bool:
        """Check if populated."""
        return "architype" in self.__dict__

    def make_stub(self: "BaseAnchor | TANCH") -> "BaseAnchor | TANCH":
        """Return unsynced copy of anchor."""
        if self.is_populated():
            unloaded = object.__new__(self.__class__)
            unloaded.name = self.name
            unloaded.id = self.id
            return unloaded
        return self

    def populate(self) -> None:
        """Retrieve the Architype from db and return."""
        from .context import JaseciContext

        jsrc = JaseciContext.get().mem

        if anchor := jsrc.find_by_id(self):
            self.__dict__.update(anchor.__dict__)
        else:
            raise ValueError(
                f"{self.__class__.__name__} [{self.ref_id}] is not a valid reference!"
            )

    def build_query(
        self,
        bulk_write: BulkWrite,
    ) -> None:
        """Save Anchor."""
        if self.state.deleted is False and self.has_write_access(self):  # type: ignore[attr-defined]
            self.state.deleted = True
            self.delete(bulk_write)
        elif not self.state.connected:
            self.state.connected = True
            self.sync_hash()
            self.insert(bulk_write)
        elif self.has_connect_access(self):  # type: ignore[attr-defined]
            self.update(bulk_write, True)

    def apply(self, session: ClientSession | None = None) -> BulkWrite:
        """Save Anchor."""
        bulk_write = BulkWrite()

        self.build_query(bulk_write)

        if bulk_write.has_operations:
            if session:
                bulk_write.execute(session)
            else:
                with (
                    BaseCollection.get_session() as session,
                    session.start_transaction(),
                ):
                    bulk_write.execute(session)

        return bulk_write

    def insert(
        self,
        bulk_write: BulkWrite,
    ) -> None:
        """Append Insert Query."""
        raise NotImplementedError("insert must be implemented in subclasses")

    def update(self, bulk_write: BulkWrite, propagate: bool = False) -> None:
        """Append Update Query."""
        changes = self.state.changes
        self.state.changes = {}  # renew reference

        operations = bulk_write.operations[self.__class__]
        operation_filter = {"_id": self.id}

        ############################################################
        #                     POPULATE CONTEXT                     #
        ############################################################
        from .context import JaseciContext

        if JaseciContext.get().root.has_write_access(self):
            set_architype = changes.pop("$set", {})
            if is_dataclass(architype := self.architype) and not isinstance(
                architype, type
            ):
                for (
                    key,
                    val,
                ) in (
                    architype.__serialize__().items()  # type:ignore[attr-defined] # mypy issue
                ):
                    if (h := hash(dumps(val))) != self.state.context_hashes.get(key):
                        self.state.context_hashes[key] = h
                        set_architype[f"architype.{key}"] = val
            if set_architype:
                changes["$set"] = set_architype
        else:
            changes.pop("$set", None)
            changes.pop("$unset", None)

        # -------------------------------------------------------- #

        if isinstance(self, NodeAnchor):
            ############################################################
            #                   POPULATE ADDED EDGES                   #
            ############################################################
            added_edges: set[BaseAnchor | Anchor] = (
                changes.get("$addToSet", {}).get("edges", {}).get("$each", [])
            )
            if added_edges:
                _added_edges = []
                for anchor in added_edges:
                    if propagate:
                        anchor.build_query(bulk_write)
                    _added_edges.append(anchor.ref_id)
                changes["$addToSet"]["edges"]["$each"] = _added_edges
            else:
                changes.pop("$addToSet", None)

            # -------------------------------------------------------- #

            ############################################################
            #                  POPULATE REMOVED EDGES                  #
            ############################################################
            pulled_edges: set[BaseAnchor | Anchor] = (
                changes.get("$pull", {}).get("edges", {}).get("$in", [])
            )
            if pulled_edges:
                _pulled_edges = []
                for anchor in pulled_edges:
                    if propagate and anchor.state.deleted is not True:
                        anchor.state.deleted = True
                        bulk_write.del_edge(anchor.id)
                    _pulled_edges.append(anchor.ref_id)

                if added_edges:
                    # Isolate pull to avoid conflict with addToSet
                    changes.pop("$pull", None)
                    operations.append(
                        UpdateOne(
                            operation_filter,
                            {"$pull": {"edges": {"$in": _pulled_edges}}},
                        )
                    )
                else:
                    changes["$pull"]["edges"]["$in"] = _pulled_edges
            else:
                changes.pop("$pull", None)

            # -------------------------------------------------------- #

        if changes:
            operations.append(UpdateOne(operation_filter, changes))

    def delete(self, bulk_write: BulkWrite) -> None:
        """Append Delete Query."""
        raise NotImplementedError("delete must be implemented in subclasses")

    def destroy(self) -> None:
        """Delete Anchor."""
        raise NotImplementedError("destroy must be implemented in subclasses")

    def has_changed(self) -> int:
        """Check if needs to update."""
        if self.state.full_hash != (new_hash := hash(pdumps(self.serialize()))):
            return new_hash
        return 0

    def sync_hash(self) -> None:
        """Sync current serialization hash."""
        if is_dataclass(architype := self.architype) and not isinstance(
            architype, type
        ):
            self.state.context_hashes = {
                key: hash(dumps(val))
                for key, val in architype.__serialize__().items()  # type:ignore[attr-defined] # mypy issue
            }
            self.state.full_hash = hash(pdumps(self.serialize()))

    def access_level(self, to: Anchor) -> AccessLevel:
        """Access validation."""
        if not to.persistent:
            return AccessLevel.WRITE

        from .context import JaseciContext

        jctx = JaseciContext.get()

        jroot = jctx.root

        # if current root is system_root
        # if current root id is equal to target anchor's root id
        # if current root is the target anchor
        if jroot == jctx.system_root or jroot.id == to.root or jroot == to:
            return AccessLevel.WRITE

        access_level = AccessLevel.NO_ACCESS

        # if target anchor have set access.all
        if (to_access := to.access).all > AccessLevel.NO_ACCESS:
            access_level = to_access.all

        # if target anchor's root have set allowed roots
        # if current root is allowed to the whole graph of target anchor's root
        if to.root and isinstance(
            to_root := jctx.mem.find_by_id(NodeAnchor.ref(f"n::{to.root}")), Anchor
        ):
            if to_root.access.all > access_level:
                access_level = to_root.access.all

            level = to_root.access.roots.check(jroot.ref_id)
            if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
                access_level = level

        # if target anchor have set allowed roots
        # if current root is allowed to target anchor
        level = to_access.roots.check(jroot.ref_id)
        if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
            access_level = level

        return access_level

    # ---------------------------------------------------------------------- #

    def report(self) -> dict[str, object]:
        """Report Anchor."""
        return {
            "id": self.ref_id,
            "context": (
                self.architype.__serialize__()  # type:ignore[attr-defined] # mypy issue
                if is_dataclass(self.architype) and not isinstance(self.architype, type)
                else {}
            ),
        }

    def serialize(self) -> dict[str, object]:
        """Serialize Anchor."""
        return {
            "_id": self.id,
            "name": self.name,
            "root": self.root,
            "access": self.access.serialize(),
            "architype": (
                self.architype.__serialize__()  # type:ignore[attr-defined] # mypy issue
                if is_dataclass(self.architype) and not isinstance(self.architype, type)
                else {}
            ),
        }

    def __repr__(self) -> str:
        """Override representation."""
        if self.is_populated():
            attrs = ""
            for f in fields(self):
                if f.name in self.__dict__:
                    attrs += f"{f.name}={self.__dict__[f.name]}, "
            attrs = attrs[:-2]
        else:
            attrs = f"name={self.name}, id={self.id}"

        return f"{self.__class__.__name__}({attrs})"


@dataclass(eq=False, repr=False, kw_only=True)
class NodeAnchor(BaseAnchor, _NodeAnchor):  # type: ignore[misc]
    """Node Anchor."""

    architype: "NodeArchitype"
    edges: list["EdgeAnchor"]

    class Collection(BaseCollection["NodeAnchor"]):
        """NodeAnchor collection interface."""

        __collection__: str | None = "node"
        __default_indexes__: list[dict] = [
            {"keys": [("_id", ASCENDING), ("name", ASCENDING), ("root", ASCENDING)]}
        ]

        @classmethod
        def __document__(cls, doc: Mapping[str, Any]) -> "NodeAnchor":
            """Parse document to NodeAnchor."""
            doc = cast(dict, doc)

            architype = architype_to_dataclass(
                NodeArchitype.__get_class__(doc.get("name") or "Root"),
                doc.pop("architype"),
            )
            anchor = NodeAnchor(
                architype=architype,
                id=doc.pop("_id"),
                edges=[e for edge in doc.pop("edges") if (e := EdgeAnchor.ref(edge))],
                access=Permission.deserialize(doc.pop("access")),
                state=AnchorState(connected=True),
                persistent=True,
                **doc,
            )
            architype.__jac__ = anchor
            anchor.sync_hash()
            return anchor

    @classmethod
    def ref(cls, ref_id: str) -> "NodeAnchor":
        """Return NodeAnchor instance if existing."""
        if match := NODE_ID_REGEX.search(ref_id):
            anchor = object.__new__(cls)
            anchor.name = str(match.group(1))
            anchor.id = ObjectId(match.group(2))
            return anchor
        raise ValueError(f"[{ref_id}] is not a valid reference!")

    def insert(
        self,
        bulk_write: BulkWrite,
    ) -> None:
        """Append Insert Query."""
        for edge in self.edges:
            edge.build_query(bulk_write)

        bulk_write.operations[NodeAnchor].append(InsertOne(self.serialize()))

    def delete(self, bulk_write: BulkWrite) -> None:
        """Append Delete Query."""
        for edge in self.edges:
            edge.delete(bulk_write)

        pulled_edges: set[EdgeAnchor] = self._pull.get("edges", {}).get("$in", [])
        for edge in pulled_edges:
            edge.delete(bulk_write)

        bulk_write.del_node(self.id)

    def destroy(self) -> None:
        """Delete Anchor."""
        if self.state.deleted is None:
            from .context import JaseciContext

            jctx = JaseciContext.get()

            if jctx.root.has_write_access(self):

                self.state.deleted = False

                for edge in self.edges:
                    edge.destroy()
                jctx.mem.remove(self.id)

    def get_edges(
        self,
        dir: EdgeDir,
        filter_func: Callable[[list["EdgeArchitype"]], list["EdgeArchitype"]] | None,
        target_obj: list["NodeArchitype"] | None,
    ) -> list["EdgeArchitype"]:
        """Get edges connected to this node."""
        from .context import JaseciContext

        JaseciContext.get().mem.populate_data(self.edges)

        return super().get_edges(dir, filter_func, target_obj)

    def edges_to_nodes(
        self,
        dir: EdgeDir,
        filter_func: Callable[[list["EdgeArchitype"]], list["EdgeArchitype"]] | None,
        target_obj: list["NodeArchitype"] | None,
    ) -> list["NodeArchitype"]:
        """Get set of nodes connected to this node."""
        from .context import JaseciContext

        JaseciContext.get().mem.populate_data(self.edges)

        return super().edges_to_nodes(dir, filter_func, target_obj)

    def serialize(self) -> dict[str, object]:
        """Serialize Node Anchor."""
        return {
            **super().serialize(),
            "edges": [edge.ref_id for edge in self.edges],
        }


@dataclass(eq=False, repr=False, kw_only=True)
class EdgeAnchor(BaseAnchor, _EdgeAnchor):  # type: ignore[misc]
    """Edge Anchor."""

    architype: "EdgeArchitype"
    source: NodeAnchor
    target: NodeAnchor
    is_undirected: bool

    class Collection(BaseCollection["EdgeAnchor"]):
        """EdgeAnchor collection interface."""

        __collection__: str | None = "edge"
        __default_indexes__: list[dict] = [
            {"keys": [("_id", ASCENDING), ("name", ASCENDING), ("root", ASCENDING)]}
        ]

        @classmethod
        def __document__(cls, doc: Mapping[str, Any]) -> "EdgeAnchor":
            """Parse document to EdgeAnchor."""
            doc = cast(dict, doc)
            architype = architype_to_dataclass(
                EdgeArchitype.__get_class__(doc.get("name") or "GenericEdge"),
                doc.pop("architype"),
            )
            anchor = EdgeAnchor(
                architype=architype,
                id=doc.pop("_id"),
                source=NodeAnchor.ref(doc.pop("source")),
                target=NodeAnchor.ref(doc.pop("target")),
                access=Permission.deserialize(doc.pop("access")),
                state=AnchorState(connected=True),
                persistent=True,
                **doc,
            )
            architype.__jac__ = anchor
            anchor.sync_hash()
            return anchor

    def __post_init__(self) -> None:
        """Populate edge to source and target."""
        # remove parent trigger
        pass

    @classmethod
    def ref(cls, ref_id: str) -> "EdgeAnchor":
        """Return EdgeAnchor instance if existing."""
        if match := EDGE_ID_REGEX.search(ref_id):
            anchor = object.__new__(cls)
            anchor.name = str(match.group(1))
            anchor.id = ObjectId(match.group(2))
            return anchor
        raise ValueError(f"{ref_id}] is not a valid reference!")

    def insert(self, bulk_write: BulkWrite) -> None:
        """Append Insert Query."""
        if source := self.source:
            source.build_query(bulk_write)

        if target := self.target:
            target.build_query(bulk_write)

        bulk_write.operations[EdgeAnchor].append(InsertOne(self.serialize()))

    def delete(self, bulk_write: BulkWrite) -> None:
        """Append Delete Query."""
        if source := self.source:
            source.build_query(bulk_write)

        if target := self.target:
            target.build_query(bulk_write)

        bulk_write.del_edge(self.id)

    def destroy(self) -> None:
        """Delete Anchor."""
        if self.state.deleted is None:
            from .context import JaseciContext

            jctx = JaseciContext.get()

            if jctx.root.has_write_access(self):
                self.state.deleted = False
                self.detach()
                jctx.mem.remove(self.id)

    def detach(self) -> None:
        """Detach edge from nodes."""
        self.source.remove_edge(self)
        self.source.disconnect_edge(self)
        self.target.remove_edge(self)
        self.target.disconnect_edge(self)

    def serialize(self) -> dict[str, object]:
        """Serialize Node Anchor."""
        return {
            **super().serialize(),
            "source": self.source.ref_id if self.source else None,
            "target": self.target.ref_id if self.target else None,
            "is_undirected": self.is_undirected,
        }


@dataclass(eq=False, repr=False, kw_only=True)
class WalkerAnchor(BaseAnchor, _WalkerAnchor):  # type: ignore[misc]
    """Walker Anchor."""

    architype: "WalkerArchitype"
    path: list[Anchor] = field(default_factory=list)
    next: list[Anchor] = field(default_factory=list)
    returns: list[Any] = field(default_factory=list)
    ignores: list[Anchor] = field(default_factory=list)
    disengaged: bool = False

    class Collection(BaseCollection["WalkerAnchor"]):
        """WalkerAnchor collection interface."""

        __collection__: str | None = "walker"
        __default_indexes__: list[dict] = [
            {"keys": [("_id", ASCENDING), ("name", ASCENDING), ("root", ASCENDING)]}
        ]

        @classmethod
        def __document__(cls, doc: Mapping[str, Any]) -> "WalkerAnchor":
            """Parse document to WalkerAnchor."""
            doc = cast(dict, doc)
            architype = architype_to_dataclass(
                WalkerArchitype.__get_class__(doc.get("name") or ""),
                doc.pop("architype"),
            )
            anchor = WalkerAnchor(
                architype=architype,
                id=doc.pop("_id"),
                access=Permission.deserialize(doc.pop("access")),
                state=AnchorState(connected=True),
                persistent=True,
                **doc,
            )
            architype.__jac__ = anchor
            anchor.sync_hash()
            return anchor

    @classmethod
    def ref(cls, ref_id: str) -> "WalkerAnchor":
        """Return EdgeAnchor instance if existing."""
        if match := WALKER_ID_REGEX.search(ref_id):
            anchor = object.__new__(cls)
            anchor.name = str(match.group(1))
            anchor.id = ObjectId(match.group(2))
            return anchor
        raise ValueError(f"{ref_id}] is not a valid reference!")

    def insert(
        self,
        bulk_write: BulkWrite,
    ) -> None:
        """Append Insert Query."""
        bulk_write.operations[WalkerAnchor].append(InsertOne(self.serialize()))

    def delete(self, bulk_write: BulkWrite) -> None:
        """Append Delete Query."""
        bulk_write.del_walker(self.id)

    def destroy(self) -> None:
        """Delete Anchor."""
        if self.state.deleted is None:
            from .context import JaseciContext

            jctx = JaseciContext.get()

            if jctx.root.has_write_access(self):
                self.state.deleted = False
                jctx.mem.remove(self.id)

    def spawn_call(self, node: Anchor) -> "WalkerArchitype":
        """Invoke data spatial call."""
        if walker := self.architype:
            self.path = []
            self.next = [node]
            self.returns = []
            while len(self.next):
                if current_node := self.next.pop(0).architype:
                    for i in current_node._jac_entry_funcs_:
                        if not i.trigger or isinstance(walker, i.trigger):
                            if i.func:
                                self.returns.append(i.func(current_node, walker))
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in walker._jac_entry_funcs_:
                        if not i.trigger or isinstance(current_node, i.trigger):
                            if i.func:
                                self.returns.append(i.func(walker, current_node))
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in walker._jac_exit_funcs_:
                        if not i.trigger or isinstance(current_node, i.trigger):
                            if i.func:
                                self.returns.append(i.func(walker, current_node))
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in current_node._jac_exit_funcs_:
                        if not i.trigger or isinstance(walker, i.trigger):
                            if i.func:
                                self.returns.append(i.func(current_node, walker))
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
            self.ignores = []
            return walker
        raise Exception(f"Invalid Reference {self.id}")


@dataclass(eq=False, repr=False, kw_only=True)
class ObjectAnchor(BaseAnchor, Anchor):  # type: ignore[misc]
    """Object Anchor."""


class BaseArchitype:
    """Architype Protocol."""

    __jac_classes__: dict[str, type["BaseArchitype"]]
    __jac_hintings__: dict[str, type]

    __jac__: Anchor

    def __serialize__(self) -> dict[str, Any]:
        """Process default serialization."""
        if is_dataclass(self) and not isinstance(self, type):
            return asdict(self)
        raise ValueError(
            f"{self.__jac__.__class__.__name__} {self.__class__.__name__} is not serializable!"
        )

    @classmethod
    def __ref_cls__(cls) -> str:
        """Get class naming."""
        return f"g:{cls.__name__}"

    @classmethod
    def __set_classes__(cls) -> dict[str, Any]:
        """Initialize Jac Classes."""
        jac_classes = {}
        for sub in cls.__subclasses__():
            sub.__jac_hintings__ = get_type_hints(sub)
            jac_classes[sub.__name__] = sub
        cls.__jac_classes__ = jac_classes

        return jac_classes

    @classmethod
    def __get_class__(cls: type[TBA], name: str) -> type[TBA]:
        """Build class map from subclasses."""
        jac_classes: dict[str, Any] | None = getattr(cls, "__jac_classes__", None)
        if not jac_classes or not (jac_class := jac_classes.get(name)):
            jac_classes = cls.__set_classes__()
            jac_class = jac_classes.get(name, cls)

        return jac_class


class NodeArchitype(BaseArchitype, _NodeArchitype):
    """Node Architype Protocol."""

    __jac__: NodeAnchor

    def __post_init__(self) -> None:
        """Create node architype."""
        self.__jac__ = NodeAnchor(
            architype=self,
            name=self.__class__.__name__,
            edges=[],
            access=Permission(),
            state=AnchorState(),
        )

    @classmethod
    def __ref_cls__(cls) -> str:
        """Get class naming."""
        return f"n:{cls.__name__}"


class EdgeArchitype(BaseArchitype, _EdgeArchitype):
    """Edge Architype Protocol."""

    __jac__: EdgeAnchor

    def __attach__(
        self,
        source: NodeAnchor,
        target: NodeAnchor,
        is_undirected: bool,
    ) -> None:
        """Attach EdgeAnchor properly."""
        jac = self.__jac__ = EdgeAnchor(
            architype=self,
            name=self.__class__.__name__,
            source=source,
            target=target,
            is_undirected=is_undirected,
            access=Permission(),
            state=AnchorState(),
        )
        source.edges.append(jac)
        target.edges.append(jac)
        source.connect_edge(jac)
        target.connect_edge(jac)

    @classmethod
    def __ref_cls__(cls) -> str:
        """Get class naming."""
        return f"e:{cls.__name__}"


class WalkerArchitype(BaseArchitype, _WalkerArchitype):
    """Walker Architype Protocol."""

    __jac__: WalkerAnchor

    def __post_init__(self) -> None:
        """Create walker architype."""
        self.__jac__ = WalkerAnchor(
            architype=self,
            name=self.__class__.__name__,
            access=Permission(),
            state=AnchorState(),
        )

    @classmethod
    def __ref_cls__(cls) -> str:
        """Get class naming."""
        return f"w:{cls.__name__}"


class ObjectArchitype(BaseArchitype, Architype):
    """Object Architype Protocol."""

    __jac__: ObjectAnchor

    def __post_init__(self) -> None:
        """Create default architype."""
        self.__jac__ = ObjectAnchor(
            architype=self,
            name=self.__class__.__name__,
            access=Permission(),
            state=AnchorState(),
        )


@dataclass(eq=False)
class GenericEdge(EdgeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]] = []
    _jac_exit_funcs_: ClassVar[list[DSFunc]] = []

    def __attach__(
        self,
        source: NodeAnchor,
        target: NodeAnchor,
        is_undirected: bool,
    ) -> None:
        """Attach EdgeAnchor properly."""
        jac = self.__jac__ = EdgeAnchor(
            architype=self,
            source=source,
            target=target,
            is_undirected=is_undirected,
            access=Permission(),
            state=AnchorState(),
        )
        source.edges.append(jac)
        target.edges.append(jac)
        source.connect_edge(jac)
        target.connect_edge(jac)


@dataclass(eq=False)
class Root(NodeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]] = []
    _jac_exit_funcs_: ClassVar[list[DSFunc]] = []

    def __post_init__(self) -> None:
        """Create node architype."""
        self.__jac__ = NodeAnchor(
            architype=self,
            edges=[],
            access=Permission(),
            state=AnchorState(),
        )
