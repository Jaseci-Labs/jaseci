"""Core primitives for Jaseci."""
from jaclang import jac_import

corelib = jac_import("corelib")
if not corelib:
    raise ImportError("Could not import primitives, internal jaseci error")

JacPlugin = corelib.JacPlugin
