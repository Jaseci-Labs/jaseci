"""Jac Language Features."""
from __future__ import annotations

from typing import Optional, TypeVar

T = TypeVar("T")


def elvis(op1: Optional[T], op2: T) -> T:
    """Jac's elvis operator feature."""
    return ret if (ret := op1) is not None else op2


# from jaclang import jac_blue_import

# prim = jac_blue_import("..core.primitives")
# if not prim:
#     raise ImportError("Could not import primitives, internal compile error")

# Object = prim.Object
# Node = prim.Node
# Edge = prim.Edge
# Walker = prim.Walker
# make_architype = prim.make_architype

# exec_ctx = prim.exec_ctx
