"""Jac Language Features."""
from __future__ import annotations


from typing import Any, Optional, Type

from jaclang.compiler.constant import EdgeDir
from jaclang.core.construct import (
    EdgeAnchor,
    GenericEdge,
    NodeAnchor,
    ObjectAnchor,
    WalkerAnchor,
    root,
)
from jaclang.plugin.spec import ArchBound, Architype, DSFunc, T


import pluggy

hookimpl = pluggy.HookimplMarker("jac")


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def bind_architype(
        arch: ArchBound,
        arch_type: str,
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> bool:
        """Create a new architype."""
        match arch_type:
            case "obj":
                arch._jac_ = ObjectAnchor(
                    obj=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "node":
                arch._jac_ = NodeAnchor(
                    obj=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "edge":
                arch._jac_ = EdgeAnchor(
                    obj=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "walker":
                arch._jac_ = WalkerAnchor(
                    obj=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case _:
                raise TypeError("Invalid archetype type")
        return True

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
        walker: Architype,
        expr: list[NodeAnchor] | list[EdgeAnchor] | NodeAnchor | EdgeAnchor,
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
            ret = node_obj._jac_.edges_to_nodes(dir, filter_type)
            print(ret)
            return ret
        else:
            raise TypeError("Invalid node object")

    @staticmethod
    @hookimpl
    def connect(
        left: Architype | list[Architype],
        right: Architype | list[Architype],
        edge_spec: Architype,
    ) -> Architype | list[Architype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        if isinstance(left, list):
            if isinstance(right, list):
                for i in left:
                    if not isinstance(i._jac_, NodeAnchor):
                        raise TypeError("Invalid node object")
                    for j in right:
                        if not isinstance(j._jac_, NodeAnchor):
                            raise TypeError("Invalid node object")
                        i._jac_.connect_node(j, edge_spec)
            else:
                for i in left:
                    if not isinstance(i._jac_, NodeAnchor):
                        raise TypeError("Invalid node object")
                    i._jac_.connect_node(right, edge_spec)
        else:
            if not isinstance(left._jac_, NodeAnchor):
                raise TypeError("Invalid node object")
            if isinstance(right, list):
                for i in right:
                    if not isinstance(i._jac_, NodeAnchor):
                        raise TypeError("Invalid node object")
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
