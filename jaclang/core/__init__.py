"""Core primitives for Jaseci."""
from jaclang import jac_import

try:
    from jaclang.core.__jac_gen__ import corelib
except Exception:
    corelib = jac_import("corelib")
if not corelib:
    raise ImportError("Could not import primitives, internal jaseci error")

JacPlugin = corelib.JacPlugin
