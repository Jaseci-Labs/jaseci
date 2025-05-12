"""Jac Language Features."""

from concurrent.futures import Future
from contextlib import suppress
from typing import Callable, Type

from jaclang.compiler.constant import EdgeDir
from jaclang.runtimelib.architype import Architype
from jaclang.runtimelib.machine import (
    JacMachineImpl,
    JacMachineInterface as Jac,
    hookimpl,
)
from jaclang.runtimelib.utils import all_issubclass

from ..core.architype import (
    AccessLevel,
    Anchor,
    AnchorState,
    BaseAnchor,
    EdgeAnchor,
    EdgeArchitype,
    GenericEdge,
    NodeAnchor,
    NodeArchitype,
    ObjectArchitype,
    Permission,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from ..core.context import JacMachine, JaseciContext
from ..jaseci.main import FastAPI


class JacAccessValidationPlugin:
    """Jac Access Validation Implementations."""

    @staticmethod
    @hookimpl
    def allow_root(
        architype: Architype, root_id: BaseAnchor, level: AccessLevel | int | str
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        if not FastAPI.is_enabled():
            JacMachineImpl.allow_root(
                architype=architype, root_id=root_id, level=level  # type: ignore[arg-type]
            )
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        access = anchor.access.roots
        if (
            isinstance(anchor, BaseAnchor)
            and (ref_id := root_id.ref_id)
            and level != access.anchors.get(ref_id)
        ):
            access.anchors[ref_id] = level
            anchor._set.update({f"access.roots.anchors.{ref_id}": level.name})
            anchor._unset.pop(f"access.roots.anchors.{ref_id}", None)

    @staticmethod
    @hookimpl
    def disallow_root(
        architype: Architype, root_id: BaseAnchor, level: AccessLevel | int | str
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        if not FastAPI.is_enabled():
            JacMachineImpl.disallow_root(
                architype=architype, root_id=root_id, level=level  # type: ignore[arg-type]
            )
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        access = anchor.access.roots
        if (
            isinstance(anchor, BaseAnchor)
            and (ref_id := root_id.ref_id)
            and access.anchors.pop(ref_id, None) is not None
        ):
            anchor._unset.update({f"access.roots.anchors.{ref_id}": True})
            anchor._set.pop(f"access.roots.anchors.{ref_id}", None)

    @staticmethod
    @hookimpl
    def perm_grant(architype: Architype, level: AccessLevel | int | str) -> None:
        """Allow everyone to access current Architype."""
        if not FastAPI.is_enabled():
            JacMachineImpl.perm_grant(architype=architype, level=level)
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        if isinstance(anchor, BaseAnchor) and level != anchor.access.all:
            anchor.access.all = level
            anchor._set.update({"access.all": level.name})

    @staticmethod
    @hookimpl
    def perm_revoke(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        if not FastAPI.is_enabled():
            JacMachineImpl.perm_revoke(architype=architype)
            return

        anchor = architype.__jac__

        if isinstance(anchor, BaseAnchor) and anchor.access.all > AccessLevel.NO_ACCESS:
            anchor.access.all = AccessLevel.NO_ACCESS
            anchor._set.update({"access.all": AccessLevel.NO_ACCESS.name})

    @staticmethod
    @hookimpl
    def check_access_level(to: Anchor) -> AccessLevel:
        """Access validation."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.check_access_level(to=to)

        if not to.persistent:
            return AccessLevel.WRITE

        from ..core.context import JaseciContext

        jctx = JaseciContext.get()

        jroot = jctx.root_state

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

            if (level := to_root.access.roots.check(jroot.ref_id)) is not None:
                access_level = level

        # if target anchor have set allowed roots
        # if current root is allowed to target anchor
        if (level := to_access.roots.check(jroot.ref_id)) is not None:
            access_level = level

        return access_level


class JacNodePlugin:
    """Jac Node Operations."""

    @staticmethod
    @hookimpl
    def get_edges(
        node: NodeAnchor,
        dir: EdgeDir,
        filter: Callable[[EdgeArchitype], bool] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacMachineImpl.get_edges(
            node=node, dir=dir, filter=filter, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )

    @staticmethod
    @hookimpl
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter: Callable[[EdgeArchitype], bool] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacMachineImpl.edges_to_nodes(
            node=node, dir=dir, filter=filter, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )


class JacEdgePlugin:
    """Jac Edge Operations."""

    @staticmethod
    @hookimpl
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        if not FastAPI.is_enabled():
            JacMachineImpl.detach(edge=edge)
            return

        Jac.remove_edge(node=edge.source, edge=edge)
        edge.source.disconnect_edge(edge)

        Jac.remove_edge(node=edge.target, edge=edge)
        edge.target.disconnect_edge(edge)


class JacPlugin(JacAccessValidationPlugin, JacNodePlugin, JacEdgePlugin):
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def setup() -> None:
        """Set Class References."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.setup()

        Jac.Obj = ObjectArchitype
        Jac.Node = NodeArchitype
        Jac.Edge = EdgeArchitype
        Jac.Walker = WalkerArchitype

        Jac.Root = Root  # type: ignore[assignment]
        Jac.GenericEdge = GenericEdge  # type: ignore[assignment]

    @staticmethod
    @hookimpl
    def get_context() -> JacMachine:
        """Get current execution context."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.get_context()

        return JaseciContext.get()

    @staticmethod
    @hookimpl
    def reset_graph(root: Root | None = None) -> int:
        """Purge current or target graph."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.reset_graph(root=root)  # type: ignore[arg-type]

        ctx = JaseciContext.get()
        ranchor = root.__jac__ if root else ctx.root_state

        deleted_count = 0  # noqa: SIM113

        for node in NodeAnchor.Collection.find(
            {"_id": {"$ne": ranchor.id}, "root": ranchor.id}
        ):
            ctx.mem.__mem__[node.id] = node
            Jac.destroy(node)
            deleted_count += 1

        for edge in EdgeAnchor.Collection.find({"root": ranchor.id}):
            ctx.mem.__mem__[edge.id] = edge
            Jac.destroy(edge)
            deleted_count += 1

        for walker in WalkerAnchor.Collection.find({"root": ranchor.id}):
            ctx.mem.__mem__[walker.id] = walker
            Jac.destroy(walker)
            deleted_count += 1

        return deleted_count

    @staticmethod
    @hookimpl
    def root() -> Root:
        """Jac's assign comprehension feature."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.root()  # type:ignore[return-value]

        return JaseciContext.get_root()

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.build_edge(  # type:ignore[return-value]
                is_undirected=is_undirected,
                conn_type=conn_type,
                conn_assign=conn_assign,
            )

        ct = conn_type if conn_type else GenericEdge

        def builder(
            source: NodeAnchor, target: NodeAnchor
        ) -> EdgeArchitype | GenericEdge:
            edge = ct() if isinstance(ct, type) else ct

            eanch = edge.__jac__ = EdgeAnchor(
                architype=edge,  # type: ignore[arg-type] # bug on mypy!!
                name=("" if isinstance(edge, GenericEdge) else edge.__class__.__name__),
                source=source,
                target=target,
                is_undirected=is_undirected,
                access=Permission(),
                state=AnchorState(),
            )
            source.edges.append(eanch)
            target.edges.append(eanch)
            source.connect_edge(eanch)
            target.connect_edge(eanch)

            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            if source.persistent or target.persistent:
                Jac.save(eanch)
            return edge  # type: ignore[return-value] # bug on mypy!!

        return builder

    @staticmethod
    @hookimpl
    def get_object(id: str) -> Architype | None:
        """Get object by id."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.get_object(id=id)

        with suppress(ValueError):
            if isinstance(architype := BaseAnchor.ref(id).architype, Architype):
                return architype

        return None

    @staticmethod
    @hookimpl
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.object_ref(obj=obj)

        return str(obj.__jac__.ref_id)

    @staticmethod
    @hookimpl
    def spawn_call(walker: WalkerAnchor, node: NodeAnchor) -> WalkerArchitype:
        """Invoke data spatial call."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.spawn_call(walker=walker, node=node)

        warch = walker.architype
        walker.path = []
        walker.next = [node]
        walker.returns = []
        current_node = node.architype

        # walker entry
        for i in warch._jac_entry_funcs_:
            if not i.trigger:
                walker.returns.append(i.func(warch, current_node))
            if walker.disengaged:
                return warch

        while len(walker.next):
            if current_node := walker.next.pop(0).architype:
                # walker entry with
                for i in warch._jac_entry_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        walker.returns.append(i.func(warch, current_node))
                    if walker.disengaged:
                        return warch

                # node entry
                for i in current_node._jac_entry_funcs_:
                    if not i.trigger:
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node entry with
                for i in current_node._jac_entry_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node exit with
                for i in current_node._jac_exit_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node exit
                for i in current_node._jac_exit_funcs_:
                    if not i.trigger:
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # walker exit with
                for i in warch._jac_exit_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        walker.returns.append(i.func(warch, current_node))
                    if walker.disengaged:
                        return warch
        # walker exit
        for i in warch._jac_exit_funcs_:
            if not i.trigger:
                walker.returns.append(i.func(warch, current_node))
            if walker.disengaged:
                return warch

        walker.ignores = []
        return warch

    @staticmethod
    @hookimpl
    def spawn(op1: Architype, op2: Architype) -> WalkerArchitype | Future:
        """Jac's spawn operator feature."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.spawn(op1=op1, op2=op2)

        if isinstance(op1, WalkerArchitype):
            walker = op1.__jac__
            if isinstance(op2, NodeArchitype):
                node = op2.__jac__
            elif isinstance(op2, EdgeArchitype):
                node = op2.__jac__.target
            else:
                raise TypeError("Invalid target object")
        elif isinstance(op2, WalkerArchitype):
            walker = op2.__jac__
            if isinstance(op1, NodeArchitype):
                node = op1.__jac__
            elif isinstance(op1, EdgeArchitype):
                node = op1.__jac__.target
            else:
                raise TypeError("Invalid target object")
        else:
            raise TypeError("Invalid walker object")

        return Jac.spawn_call(walker=walker, node=node)  # type: ignore[return-value]

    @staticmethod
    @hookimpl
    def destroy(
        objs: Architype | Anchor | BaseAnchor | list[Architype | Anchor | BaseAnchor],
    ) -> None:
        """Destroy object."""
        if not FastAPI.is_enabled():
            return JacMachineImpl.destroy(objs=objs)
        obj_list = objs if isinstance(objs, list) else [objs]
        for obj in obj_list:
            if not isinstance(obj, (Architype, Anchor)):
                return
            anchor = obj.__jac__ if isinstance(obj, Architype) else obj

            if (
                isinstance(anchor, BaseAnchor)
                and anchor.state.deleted is None
                and Jac.check_write_access(anchor)  # type: ignore[arg-type]
            ):
                anchor.state.deleted = False
                match anchor:
                    case NodeAnchor():
                        for edge in anchor.edges:
                            Jac.destroy(edge)
                    case EdgeAnchor():
                        Jac.detach(anchor)
                    case _:
                        pass

                Jac.get_context().mem.remove(anchor.id)
