"""The Jac Programming Language."""

import inspect
import os
from abc import abstractmethod as abstract
from dataclasses import field as dc_field
from types import ModuleType
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Type,
    TypeGuard,
    TypeVar,
    cast,
    override,
)

from jaclang.plugin.builtin import dotgen, jid, jobj  # noqa: F401
from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature as Jac, plugin_manager
from jaclang.plugin.spec import EdgeDir

__all__ = [
    # Jac types.
    "Obj",
    "Walker",
    "Node",
    "Edge",
    "JacList",
    "EdgeDir",
    "Root",
    # Decorators.
    "with_entry",
    "with_exit",
    "jac_test",
    "abstract",
    "override",
    # Functions.
    "jac_import",
    "field",
    # Builtin.
    "Jac",
    "root",
    "static",
    "dotgen",
    "jid",
    "jobj",
]


# ----------------------------------------------------------------------------
# Plugin Initialization.
# ----------------------------------------------------------------------------

plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")

T = TypeVar("T")
S = TypeVar("S")  # S is a subtype of T.

# ----------------------------------------------------------------------------
# Meta classes.
# ----------------------------------------------------------------------------


class JacList(Generic[T], list[T]):
    """List with jac methods."""

    def filter(
        self,
        ty: Type[S] | None = None,
        fn: Callable[[T | S], TypeGuard[S]] | None = None,
    ) -> "JacList[S]":
        """Filter comprehension."""
        if ty and fn:
            return JacList([item for item in self if isinstance(item, ty) and fn(item)])
        if ty:
            return JacList([item for item in self if isinstance(item, ty)])
        if fn:
            return JacList(list(filter(fn, self)))
        return cast(JacList[S], self)

    def assign(self, attrs: tuple[str], values: tuple[Any]) -> "JacList[T]":
        """Assign Comprehension."""
        return JacList(Jac.assign_compr(self, (attrs, values)))


# ----------------------------------------------------------------------------
# Decorators.
# ----------------------------------------------------------------------------


def with_entry(func: Callable) -> Callable:
    """Mark a method as jac entry with this decorator."""
    setattr(func, "__jac_entry", True)  # noqa: B010
    return func


def with_exit(func: Callable) -> Callable:
    """Mark a method as jac exit with this decorator."""
    setattr(func, "__jac_exit", True)  # noqa: B010
    return func


# ----------------------------------------------------------------------------
# Functions.
# ----------------------------------------------------------------------------


def jac_import(
    target: str,
    lng: str | None = "jac",
    base_path: str | None = None,
    absorb: bool = False,
    cachable: bool = True,
    alias: str | None = None,
    override_name: str | None = None,
    items: dict[str, str | None] | None = None,
    reload_module: bool | None = False,
) -> tuple[ModuleType, ...]:
    """Import a module."""
    base_path = base_path or os.path.dirname(inspect.stack()[1].filename)
    return Jac.jac_import(
        target=target,
        lng=lng,
        base_path=base_path,
        absorb=absorb,
        cachable=cachable,
        mdl_alias=alias,
        override_name=override_name,
        items=items,
        reload_module=reload_module,
    )


def field(
    value: T = None,  # type: ignore [assignment]
    gen: Callable[[], T] | None = None,
    postinit: bool = False,
) -> T:
    """Set the default value to jac architype dataclass."""
    if postinit:
        return dc_field(init=False)
    gen = gen or (lambda: value)  # noqa: E731
    return Jac.has_instance_default(gen_func=gen)  # type: ignore


# ----------------------------------------------------------------------------
# Builtin.
# ----------------------------------------------------------------------------

jac_test = Jac.create_test
static = ClassVar
