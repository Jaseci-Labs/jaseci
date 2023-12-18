"""Jac Language Features."""
from __future__ import annotations


from typing import Any, Optional, Type

from jaclang.jac.constant import EdgeDir
from jaclang.jac.plugin.spec import AT, Architype, ArchitypeProtocol, DSFunc, T

import pluggy

hookimpl = pluggy.HookimplMarker("jac")


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def bind_architype(
        arch: Type[AT], arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> bool:
        """Create a new architype."""

        class DummyAP(ArchitypeProtocol):
            ds_entry_funcs: list[DSFunc] = on_entry
            ds_exit_funcs: list[DSFunc] = on_exit

        arch._jac_ = DummyAP()
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
    def visit(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
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
    def connect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return ret if (ret := op1) is not None else op2

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

        class Blank(Architype):
            _jac_: Any = None

        return Blank()
