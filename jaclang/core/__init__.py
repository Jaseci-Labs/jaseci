"""Core primitives for Jaseci."""
from jaclang import jac_blue_import

prim = jac_blue_import("primitives")


Object = prim.Object
Node = prim.Node
Edge = prim.Edge
Walker = prim.Walker

exec_ctx = prim.exec_ctx
