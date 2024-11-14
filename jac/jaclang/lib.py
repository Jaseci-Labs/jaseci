"""Jac python interface."""

import inspect
import typing

from .plugin.feature import JacFeature as _Jac
from dataclasses import dataclass as __jac_dataclass__


# ----------------------------------------------------------------------------
# Meta classes.
# ----------------------------------------------------------------------------

class JacMetaCommon(type):
    """Common metaclass for Jac types."""

    def __new__(cls, name, bases, dct, make_func):

        on_entry, on_exit = [], []
        for name, value in dct.items():
            if hasattr(value, "__jac_entry"):
                entry_node = getattr(value, "__jac_entry")
                on_entry.append(_Jac.DSFunc(value.__name__, entry_node))
            if hasattr(value, "__jac_exit"):
                exit_node = getattr(value, "__jac_exit")
                on_exit.append(_Jac.DSFunc(value.__name__, exit_node))

        cls = super().__new__(cls, name, bases, dct)
        cls = __jac_dataclass__(eq=False)(cls)
        cls = make_func(on_entry=on_entry, on_exit=on_exit)(cls)
        return cls

class JacMetaObj(JacMetaCommon):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct, _Jac.make_obj)

class JacMetaWalker(JacMetaCommon):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct, _Jac.make_walker)

class JacMetaNode(JacMetaCommon):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct, _Jac.make_node)

class JacMetaEdge(JacMetaCommon):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct, _Jac.make_edge)

# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------

# https://stackoverflow.com/a/9639512/10846399
class _JacArchiTypeBase:
    pass

class JacObj(_JacArchiTypeBase, metaclass=JacMetaObj):
    pass

class JacWalker(_JacArchiTypeBase, metaclass=JacMetaWalker):
    def spawn(self, node):
        _Jac.spawn_call(self, node)

class JacNode(_JacArchiTypeBase, metaclass=JacMetaNode):
    def spawn(self, walker):
        _Jac.spawn_call(self, walker)

class JacEdge(_JacArchiTypeBase, metaclass=JacMetaEdge):
    pass

# ----------------------------------------------------------------------------
# Decorators.
# ----------------------------------------------------------------------------

def with_entry(func):
    """Decorator to mark a method as jac entry."""

    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac entry function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    entry_node = typing.get_type_hints(func).get(second_param_name, None)

    # Mark the function as jac entry.
    setattr(func, "__jac_entry", entry_node)
    return func


def with_exit(func):
    """Decorator to mark a method as jac exit."""

    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac exit function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    exit_node = typing.get_type_hints(func).get(second_param_name, None)

    # Mark the function as jac entry.
    setattr(func, "__jac_exit", exit_node)
    return func


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------

spawn = _Jac.spawn_call

def connect(node_from, node_to, edge=None, unidir=False):
    return _Jac.connect(
        left=node_from,
        right=node_to,
        edge_spec=_Jac.build_edge(is_undirected=unidir,
                                  conn_type=edge,
                                  conn_assign=None))
