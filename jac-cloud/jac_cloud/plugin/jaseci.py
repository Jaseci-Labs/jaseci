"""Jac Language Features."""

from collections import OrderedDict
from contextlib import suppress
from functools import wraps
from typing import Callable, Type

from jaclang.compiler.constant import EdgeDir
from jaclang.plugin.default import (
    JacCallableImplementation as _JacCallableImplementation,
    JacFeatureImpl,
    hookimpl,
)
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.architype import Architype, DSFunc
from jaclang.runtimelib.utils import all_issubclass

from .implementation.api import populate_apis
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
from ..core.context import ExecutionContext, JaseciContext
from ..jaseci import FastAPI


class JacCallableImplementation:
    """Callable Implementations."""

    @staticmethod
    def get_object(id: str) -> Architype | None:
        """Get object by id."""
        if not FastAPI.is_enabled():
            return _JacCallableImplementation.get_object(id=id)

        with suppress(ValueError):
            if isinstance(architype := BaseAnchor.ref(id).architype, Architype):
                return architype

        return None


class JacAccessValidationPlugin:
    """Jac Access Validation Implementations."""

    @staticmethod
    @hookimpl
    def allow_root(
        architype: Architype, root_id: BaseAnchor, level: AccessLevel | int | str
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.allow_root(
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
            JacFeatureImpl.disallow_root(
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
    def unrestrict(architype: Architype, level: AccessLevel | int | str) -> None:
        """Allow everyone to access current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.unrestrict(architype=architype, level=level)
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        if isinstance(anchor, BaseAnchor) and level != anchor.access.all:
            anchor.access.all = level
            anchor._set.update({"access.all": level.name})

    @staticmethod
    @hookimpl
    def restrict(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.restrict(architype=architype)
            return

        anchor = architype.__jac__

        if isinstance(anchor, BaseAnchor) and anchor.access.all > AccessLevel.NO_ACCESS:
            anchor.access.all = AccessLevel.NO_ACCESS
            anchor._set.update({"access.all": AccessLevel.NO_ACCESS.name})

    @staticmethod
    @hookimpl
    def check_access_level(to: Anchor, no_custom: bool) -> AccessLevel:
        """Access validation."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.check_access_level(to=to, no_custom=no_custom)

        if not to.persistent:
            return AccessLevel.WRITE

        from ..core.context import JaseciContext

        jctx = JaseciContext.get()

        jroot = jctx.root

        # if current root is system_root
        # if current root id is equal to target anchor's root id
        # if current root is the target anchor
        if jroot == jctx.system_root or jroot.id == to.root or jroot == to:
            return AccessLevel.WRITE

        if (
            not no_custom
            and (custom_level := to.architype.__jac_access__()) is not None
        ):
            return AccessLevel.cast(custom_level)

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
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacFeatureImpl.get_edges(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )

    @staticmethod
    @hookimpl
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacFeatureImpl.edges_to_nodes(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )


class JacEdgePlugin:
    """Jac Edge Operations."""

    @staticmethod
    @hookimpl
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.detach(edge=edge)
            return

        Jac.remove_edge(node=edge.source, edge=edge)
        edge.source.disconnect_edge(edge)

        Jac.remove_edge(node=edge.target, edge=edge)
        edge.target.disconnect_edge(edge)


class JacPlugin(JacAccessValidationPlugin, JacNodePlugin, JacEdgePlugin):
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_context()

        return JaseciContext.get()

    @staticmethod
    @hookimpl
    def reset_graph(root: Root | None = None) -> int:
        """Purge current or target graph."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.reset_graph(root=root)  # type: ignore[arg-type]

        ctx = JaseciContext.get()
        ranchor = root.__jac__ if root else ctx.root

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
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_architype(
                cls=cls, arch_base=arch_base, on_entry=on_entry, on_exit=on_exit
            )
        for i in on_entry + on_exit:
            i.resolve(cls)
        if not hasattr(cls, "_jac_entry_funcs_") or not hasattr(
            cls, "_jac_exit_funcs_"
        ):
            # Saving the module path and reassign it after creating cls
            # So the jac modules are part of the correct module
            cur_module = cls.__module__
            cls = type(cls.__name__, (cls, arch_base), {})
            cls.__module__ = cur_module
            cls._jac_entry_funcs_ = on_entry  # type: ignore
            cls._jac_exit_funcs_ = on_exit  # type: ignore
        else:
            new_entry_funcs = OrderedDict(zip([i.name for i in on_entry], on_entry))
            entry_funcs = OrderedDict(
                zip([i.name for i in cls._jac_entry_funcs_], cls._jac_entry_funcs_)
            )
            entry_funcs.update(new_entry_funcs)
            cls._jac_entry_funcs_ = list(entry_funcs.values())

            new_exit_funcs = OrderedDict(zip([i.name for i in on_exit], on_exit))
            exit_funcs = OrderedDict(
                zip([i.name for i in cls._jac_exit_funcs_], cls._jac_exit_funcs_)
            )
            exit_funcs.update(new_exit_funcs)
            cls._jac_exit_funcs_ = list(exit_funcs.values())

        inner_init = cls.__init__  # type: ignore

        @wraps(inner_init)
        def new_init(self: Architype, *args: object, **kwargs: object) -> None:
            arch_base.__init__(self)
            inner_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_obj(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls,
                arch_base=ObjectArchitype,
                on_entry=on_entry,
                on_exit=on_exit,
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_node(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_edge(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_walker(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls,
                arch_base=WalkerArchitype,
                on_entry=on_entry,
                on_exit=on_exit,
            )
            populate_apis(cls)  # type: ignore[arg-type]
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_root()  # type:ignore[return-value]

        return JaseciContext.get_root()

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_root_type()  # type:ignore[return-value]

        return Root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.build_edge(  # type:ignore[return-value]
                is_undirected=is_undirected,
                conn_type=conn_type,
                conn_assign=conn_assign,
            )

        conn_type = conn_type if conn_type else GenericEdge

        def builder(source: NodeAnchor, target: NodeAnchor) -> EdgeArchitype:
            edge = conn_type() if isinstance(conn_type, type) else conn_type

            eanch = edge.__jac__ = EdgeAnchor(
                architype=edge,
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
                Jac.save(target)
                Jac.save(source)
            return edge

        return builder

    @staticmethod
    @hookimpl
    def get_object_func() -> Callable[[str], Architype | None]:
        """Get object by id func."""
        return JacCallableImplementation.get_object

    @staticmethod
    @hookimpl
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.object_ref(obj=obj)

        return str(obj.__jac__.ref_id)

    @staticmethod
    @hookimpl
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Invoke data spatial call."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.spawn_call(
                op1=op1, op2=op2
            )  # type:ignore[return-value]

        if isinstance(op1, WalkerArchitype):
            warch = op1
            walker = op1.__jac__
            if isinstance(op2, NodeArchitype):
                node = op2.__jac__
            elif isinstance(op2, EdgeArchitype):
                node = op2.__jac__.target
            else:
                raise TypeError("Invalid target object")
        elif isinstance(op2, WalkerArchitype):
            warch = op2
            walker = op2.__jac__
            if isinstance(op1, NodeArchitype):
                node = op1.__jac__
            elif isinstance(op1, EdgeArchitype):
                node = op1.__jac__.target
            else:
                raise TypeError("Invalid target object")
        else:
            raise TypeError("Invalid walker object")

        walker.path = []
        walker.next = [node]
        walker.returns = []
        current_node = node.architype

        # walker entry
        for i in warch._jac_entry_funcs_:
            if i.func and not i.trigger:
                walker.returns.append(i.func(warch, current_node))
            if walker.disengaged:
                return warch

        while len(walker.next):
            if current_node := walker.next.pop(0).architype:
                # walker entry with
                for i in warch._jac_entry_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        walker.returns.append(i.func(warch, current_node))
                    if walker.disengaged:
                        return warch

                # node entry
                for i in current_node._jac_entry_funcs_:
                    if i.func and not i.trigger:
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node entry with
                for i in current_node._jac_entry_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node exit with
                for i in current_node._jac_exit_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # node exit
                for i in current_node._jac_exit_funcs_:
                    if i.func and not i.trigger:
                        walker.returns.append(i.func(current_node, warch))
                    if walker.disengaged:
                        return warch

                # walker exit with
                for i in warch._jac_exit_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        walker.returns.append(i.func(warch, current_node))
                    if walker.disengaged:
                        return warch
        # walker exit
        for i in warch._jac_exit_funcs_:
            if i.func and not i.trigger:
                walker.returns.append(i.func(warch, current_node))
            if walker.disengaged:
                return warch

        walker.ignores = []
        return warch

    @staticmethod
    @hookimpl
    def destroy(obj: Architype | Anchor | BaseAnchor) -> None:
        """Destroy object."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.destroy(obj=obj)  # type:ignore[arg-type]

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
