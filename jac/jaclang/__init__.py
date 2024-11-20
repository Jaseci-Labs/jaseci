"""The Jac Programming Language."""

__all__ = [
    "JacObj",
    "JacWalker",
    "JacNode",
    "JacEdge",
    "with_entry",
    "with_exit",
    "abstractmethod",
    "jac_import",
    "root",
]

import inspect
import types
import typing
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple, Type

from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature as _Jac, plugin_manager

# ----------------------------------------------------------------------------
# Plugin Initialization.
# ----------------------------------------------------------------------------

plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")


# ----------------------------------------------------------------------------
# Meta classes.
# ----------------------------------------------------------------------------


# https://stackoverflow.com/a/9639512/10846399
class _JacArchiTypeBase:
    pass


class JacMetaCommon(ABCMeta):
    """Common metaclass for Jac types."""

    def __new__(
        cls,
        name: str,
        bases: Tuple[Type, ...],
        dct: Dict[str, Any],
        make_func: Callable[[list, list], Callable[[type], type]],
    ) -> "JacMetaCommon":

        # We have added this "__init__" to the jac base class just to make the type checkers happy.
        # Actually the dataclass decorator will create an __init__ function and assign it here bellow.
        if bases == (_JacArchiTypeBase,) and "__init__" in dct:
            del dct["__init__"]

        on_entry, on_exit = [], []
        for value in dct.values():
            if hasattr(value, "__jac_entry"):
                entry_node = getattr(value, "__jac_entry")  # noqa: B009
                on_entry.append(_Jac.DSFunc(value.__name__, entry_node))
            if hasattr(value, "__jac_exit"):
                exit_node = getattr(value, "__jac_exit")  # noqa: B009
                on_exit.append(_Jac.DSFunc(value.__name__, exit_node))

        inst = super().__new__(cls, name, bases, dct)
        inst = dataclass(eq=False)(inst)  # type: ignore [arg-type, assignment]
        inst = make_func(on_entry, on_exit)(inst)  # type: ignore [assignment]
        return inst


class JacMetaObj(JacMetaCommon, ABC):
    def __new__(
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_obj)


class JacMetaWalker(JacMetaCommon, ABC):
    def __new__(
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_walker)


class JacMetaNode(JacMetaCommon, ABC):
    def __new__(
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_node)


class JacMetaEdge(JacMetaCommon, ABC):
    def __new__(
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_edge)


# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------


class JacObj(_JacArchiTypeBase, metaclass=JacMetaObj):
    """Base class for all the jac object types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


class JacWalker(_JacArchiTypeBase, metaclass=JacMetaWalker):
    """Base class for all the jac walker types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, node: "JacNode") -> None:  # REVIEW: What should it return?
        """Spawn a new node from the walker."""
        _Jac.spawn_call(self, node)  # type: ignore [arg-type]


class JacNode(_JacArchiTypeBase, metaclass=JacMetaNode):
    """Base class for all the jac node types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, walker: JacWalker) -> None:  # REVIEW: What should it return?
        """Spawn a new node from the walker."""
        _Jac.spawn_call(self, walker)  # type: ignore [arg-type]

    def connect(
        self,
        node: "JacNode",
        edge: "type[JacEdge] | JacEdge | None" = None,
        unidir: bool = False,
    ) -> "JacNode":
        """Connect the current node to another node."""
        # TODO: The above edge type should be reviewed, as the bellow can also take None, Edge, type[Edge].
        _Jac.connect(
            left=self,  # type: ignore [arg-type]
            right=node,  # type: ignore [arg-type]
            edge_spec=_Jac.build_edge(
                is_undirected=unidir, conn_type=edge, conn_assign=None  # type: ignore [arg-type]
            ),
        )
        return node


class JacEdge(_JacArchiTypeBase, metaclass=JacMetaEdge):
    """Base class for all the jac edge types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


# ----------------------------------------------------------------------------
# Decorators.
# ----------------------------------------------------------------------------


def with_entry(func: Callable) -> Callable:
    """Mark a method as jac entry with this decorator."""
    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func, eval_str=True)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac entry function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    entry_node = typing.get_type_hints(func).get(second_param_name)

    # Mark the function as jac entry.
    setattr(func, "__jac_entry", entry_node)  # noqa: B010
    return func


def with_exit(func: Callable) -> Callable:
    """Mark a method as jac exit with this decorator."""
    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func, eval_str=True)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac exit function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    exit_node = typing.get_type_hints(func).get(second_param_name)

    # Mark the function as jac entry.
    setattr(func, "__jac_exit", exit_node)  # noqa: B010
    return func


# ----------------------------------------------------------------------------
# Functions.
# ----------------------------------------------------------------------------

jac_import = _Jac.jac_import
root = _Jac.get_root()

root.spawn = types.MethodType(JacNode.spawn, root)
root.connect = types.MethodType(JacNode.connect, root)
