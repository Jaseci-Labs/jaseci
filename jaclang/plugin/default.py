"""Jac Language Features."""
from __future__ import annotations


from typing import Any, Optional, Type

from jaclang.compiler.constant import EdgeDir
from jaclang.core.construct import EdgeAnchor, NodeAnchor, ObjectAnchor, WalkerAnchor
from jaclang.plugin.spec import AT, Architype, DSFunc, T


import pluggy

hookimpl = pluggy.HookimplMarker("jac")


class BlankArch(Architype):
    """Blank Architype."""

    _jac_: Any = None


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def bind_architype(
        arch: Type[AT], arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> bool:
        """Create a new architype."""
        match arch_type:
            case "obj":
                arch._jac_ = ObjectAnchor(
                    ob=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "node":
                arch._jac_ = NodeAnchor(
                    ob=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "edge":
                arch._jac_ = EdgeAnchor(
                    ob=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case "walker":
                arch._jac_ = WalkerAnchor(
                    ob=arch, ds_entry_funcs=on_entry, ds_exit_funcs=on_exit
                )
            case _:
                raise TypeError("Invalid archetype type")
        return True

    @staticmethod
    @hookimpl
    def elvis(op1: Optional[T], op2: T) -> T:  # noqa: ANN401
        """Jac's elvis operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    @hookimpl
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""

    @staticmethod
    @hookimpl
    def ignore(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def visit_node(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def disengage(walker_obj: Any) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def edge_ref(
        node_obj: Any,  # noqa: ANN401
        dir: EdgeDir,
        filter_type: Optional[type],
    ) -> list[Any]:  # noqa: ANN401
        """Jac's apply_dir stmt feature."""
        return []

    @staticmethod
    @hookimpl
    def connect(
        left: T, right: T, edge_spec: tuple[int, Optional[type], Optional[tuple]]
    ) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return ret if (ret := left) is not None else right

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
        return BlankArch()

    @staticmethod
    @hookimpl
    def build_edge(
        edge_spec: tuple[int, Optional[tuple], Optional[tuple]]
    ) -> Architype:
        """Jac's root getter."""
        return BlankArch()
