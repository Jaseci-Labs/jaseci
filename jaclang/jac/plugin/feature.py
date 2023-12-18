"""Jac Language Features."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Type

from jaclang.jac.constant import EdgeDir
from jaclang.jac.plugin.default import JacFeatureDefaults
from jaclang.jac.plugin.spec import (
    AT,
    AbsRootHook,
    Architype,
    JacFeatureSpec,
    T,
)

import pluggy


class JacFeature:
    """Jac Feature."""

    from jaclang.jac.plugin.spec import DSFunc

    pm = pluggy.PluginManager("jac")
    pm.add_hookspecs(JacFeatureSpec)
    pm.register(JacFeatureDefaults)

    RootType: Type[AbsRootHook] = AbsRootHook

    @staticmethod
    def make_architype(
        arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[AT]) -> Type[AT]:
            """Decorate class."""
            cls = dataclass(eq=False)(cls)
            for i in on_entry + on_exit:
                i.resolve(cls)
            if not issubclass(cls, Architype):
                cls = type(cls.__name__, (cls, Architype), {})
            JacFeature.bind_architype(cls, arch_type, on_entry, on_exit)
            return cls

        return decorator

    @staticmethod
    def bind_architype(
        arch: Type[AT], arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> bool:
        """Create a new architype."""
        return JacFeature.pm.hook.bind_architype(
            arch=arch, arch_type=arch_type, on_entry=on_entry, on_exit=on_exit
        )

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
    def visit_node(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return JacFeature.pm.hook.visit_node(walker_obj=walker_obj, expr=expr)

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
    def connect(
        left: T, right: T, edge_spec: tuple[int, Optional[type], Optional[tuple]]
    ) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return JacFeature.pm.hook.connect(left=left, right=right, edge_spec=edge_spec)

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

    @staticmethod
    def get_root() -> Architype:
        """Jac's assign comprehension feature."""
        return JacFeature.pm.hook.get_root()

    @staticmethod
    def build_edge(
        edge_spec: tuple[int, Optional[tuple], Optional[tuple]]
    ) -> Architype:
        """Jac's root getter."""
        return JacFeature.pm.hook.build_edge(edge_spec=edge_spec)
