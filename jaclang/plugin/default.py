"""Jac Language Features."""
from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional, Type


from jaclang.plugin.spec import (
    EdgeAnchor,
    GenericEdge,
    NodeAnchor,
    ObjectAnchor,
    WalkerAnchor,
    NodeArchitype,
    EdgeArchitype,
    WalkerArchitype,
    Architype,
    DSFunc,
    EdgeDir,
    root,
    ArchBound,
    T,
)


import pluggy

hookimpl = pluggy.HookimplMarker("jac")


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def make_architype(
        arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[ArchBound]) -> Type[ArchBound]:
            """Decorate class."""
            cls = dataclass(eq=False)(cls)
            for i in on_entry + on_exit:
                i.resolve(cls)
            if not issubclass(cls, Architype):
                match arch_type:
                    case "obj":
                        ArchClass = Architype
                    case "node":
                        ArchClass = NodeArchitype
                    case "edge":
                        ArchClass = EdgeArchitype
                    case "walker":
                        ArchClass = WalkerArchitype
                    case _:
                        raise TypeError("Invalid archetype type")
                cls = type(cls.__name__, (cls, ArchClass), {})
                cls._jac_entry_funcs_ = on_entry
                cls._jac_exit_funcs_ = on_exit
                original_init = cls.__init__

                @wraps(original_init)
                def new_init(self, *args, **kwargs) -> None:
                    original_init(self, *args, **kwargs)
                    ArchClass.__init__(self)

                cls.__init__ = new_init
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    @hookimpl
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""

    @staticmethod
    @hookimpl
    def ignore(
        walker: WalkerAnchor,
        expr: list[NodeAnchor] | list[EdgeAnchor] | NodeAnchor | EdgeAnchor,
    ) -> bool:
        """Jac's ignore stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def visit_node(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Jac's visit stmt feature."""
        if isinstance(walker._jac_, WalkerAnchor):
            return walker._jac_.visit_node(expr)
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def disengage(walker: WalkerAnchor) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def edge_ref(
        node_obj: Architype,
        dir: EdgeDir,
        filter_type: Optional[type],
    ) -> list[Architype]:
        """Jac's apply_dir stmt feature."""
        if isinstance(node_obj._jac_, NodeAnchor):
            return node_obj._jac_.edges_to_nodes(dir, filter_type)
        else:
            raise TypeError("Invalid node object")

    @staticmethod
    @hookimpl
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: EdgeArchitype,
    ) -> NodeArchitype | list[NodeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        if isinstance(left, list):
            if isinstance(right, list):
                for i in left:
                    for j in right:
                        i._jac_.connect_node(j, edge_spec)
            else:
                for i in left:
                    i._jac_.connect_node(right, edge_spec)
        else:
            if isinstance(right, list):
                for i in right:
                    left._jac_.connect_node(i, edge_spec)
            else:
                left._jac_.connect_node(right, edge_spec)
        return left

    @staticmethod
    @hookimpl
    def disconnect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    @hookimpl
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""
        return target

    @staticmethod
    @hookimpl
    def get_root() -> Architype:
        """Jac's assign comprehension feature."""
        return root

    @staticmethod
    @hookimpl
    def build_edge(
        edge_dir: EdgeDir,
        conn_type: Optional[Type[Architype]],
        conn_assign: Optional[tuple],
    ) -> Architype:
        """Jac's root getter."""
        conn_type = conn_type if conn_type else GenericEdge
        edge = conn_type()
        if isinstance(edge._jac_, EdgeAnchor):
            edge._jac_.dir = edge_dir
        else:
            raise TypeError("Invalid edge object")
        return edge
