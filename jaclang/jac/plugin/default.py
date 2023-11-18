"""Jac Language Features."""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from types import FunctionType, MethodType
from typing import Any, Callable, Optional, Protocol, Type, TypeVar

from jaclang.jac.constant import EdgeDir
from jaclang.jac.plugin import hookimpl


class ArchitypeProtocol(Protocol):
    """Architype Protocol."""

    _jac_: None


T = TypeVar("T")
AT = TypeVar("AT", bound=ArchitypeProtocol)


class JacFeatureDefaults:
    """Jac Feature."""

    @staticmethod
    @hookimpl
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[AT]) -> Type[AT]:
            """Decorate class."""
            for attr_name, attr_value in cls.__dict__.items():
                func_types = (FunctionType, MethodType, classmethod, staticmethod)
                if isinstance(attr_value, func_types) and not attr_name.startswith(
                    "__"
                ):
                    new_method_name = f"{arch_type[0]}_{cls.__name__}_c_{attr_name}"  # TODO: Generalize me
                    cls_module_globals = inspect.getmodule(cls).__dict__
                    # Check if a function with the new name exists in the global scope
                    if new_method_name in cls_module_globals:
                        setattr(cls, attr_name, cls_module_globals[new_method_name])
                        func_module_globals = cls_module_globals[
                            new_method_name
                        ].__globals__
                        for k, v in cls_module_globals.items():  # Risky!
                            if k not in func_module_globals and not k.startswith("__"):
                                func_module_globals[k] = v
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
