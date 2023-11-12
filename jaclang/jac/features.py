"""Jac Language Features."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol, Type, TypeVar

from jaclang.jac import hookimpl
from jaclang.jac.constant import EdgeDir

import pluggy

hookspec = pluggy.HookspecMarker("jac")


class ArchitypeProtocol(Protocol):
    """Architype Protocol."""

    _jac_: None


T = TypeVar("T")
AT = TypeVar("AT", bound=ArchitypeProtocol)


class JacFeatureSpec:
    """Jac Feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""

    @staticmethod
    @hookspec(firstresult=True)
    def make_ds_ability(event: str, trigger: Optional[type]) -> Callable[[type], type]:
        """Create a new architype."""

    @staticmethod
    @hookspec(firstresult=True)
    def elvis(op1: Optional[T], op2: T) -> T:  # noqa: ANN401
        """Jac's elvis operator feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def ignore(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def visit(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return True

    @staticmethod
    @hookspec(firstresult=True)
    def disengage(walker_obj: Any) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def edge_ref(
        node_obj: Any, dir: EdgeDir, filter_type: Optional[type]  # noqa: ANN401
    ) -> list[Any]:
        """Jac's apply_dir stmt feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def connect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """

    @staticmethod
    @hookspec(firstresult=True)
    def disconnect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[AT]) -> Type[AT]:
            """Decorate class."""
            cls._jac_ = None
            return dataclass(cls)

        return decorator

    @staticmethod
    @hookimpl
    def make_ds_ability(event: str, trigger: Optional[type]) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(func: type) -> type:
            """Decorate class."""
            return func

        return decorator

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

    @staticmethod
    @hookimpl
    def visit(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return True

    @staticmethod
    @hookimpl
    def disengage(walker_obj: Any) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""

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


class JacFeature:
    """Jac Feature."""

    pm = pluggy.PluginManager("jac")
    pm.add_hookspecs(JacFeatureSpec)
    pm.load_setuptools_entrypoints("jac")
    pm.register(JacFeatureDefaults)

    @staticmethod
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""
        return JacFeature.pm.hook.make_architype(arch_type=arch_type)

    @staticmethod
    def make_ds_ability(event: str, trigger: Optional[type]) -> Callable[[type], type]:
        """Create a new architype."""
        return JacFeature.pm.hook.make_ds_ability(event=event, trigger=trigger)

    @staticmethod
    def elvis(op1: Optional[T], op2: T) -> T:  # noqa: ANN401
        """Jac's elvis operator feature."""
        return JacFeature.pm.hook.elvis(op1=op1, op2=op2)

    @staticmethod
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        return JacFeature.pm.hook.report(expr=expr)

    @staticmethod
    def ignore(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        return JacFeature.pm.hook.ignore(walker_obj=walker_obj, expr=expr)

    @staticmethod
    def visit(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return JacFeature.pm.hook.visit(walker_obj=walker_obj, expr=expr)

    @staticmethod
    def disengage(walker_obj: Any) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        return JacFeature.pm.hook.disengage(walker_obj=walker_obj)

    @staticmethod
    def edge_ref(
        node_obj: Any,  # noqa: ANN401
        dir: EdgeDir,
        filter_type: Optional[type],
    ) -> list[Any]:  # noqa: ANN401
        """Jac's apply_dir stmt feature."""
        return JacFeature.pm.hook.edge_ref(
            node_obj=node_obj, dir=dir, filter_type=filter_type
        )

    @staticmethod
    def connect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return JacFeature.pm.hook.connect(op1=op1, op2=op2, op=op)

    @staticmethod
    def disconnect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""
        return JacFeature.pm.hook.disconnect(op1=op1, op2=op2, op=op)

    @staticmethod
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""
        return JacFeature.pm.hook.assign_compr(target=target, attr_val=attr_val)
