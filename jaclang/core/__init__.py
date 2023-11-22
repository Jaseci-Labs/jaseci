"""Core primitives for Jaseci."""
from jaclang import jac_import

prim = jac_import("corelib")
if not prim:
    raise ImportError("Could not import primitives, internal compile error")

JacPlugin = prim.JacPlugin
