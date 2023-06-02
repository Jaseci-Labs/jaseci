"""Transpilation pass for Jaseci Ast."""
from jaseci.jac.passes.ir_pass import AstNode, Pass


# MACROS for rapid development
MAST = "active_master"
MAST_PATH = "jaseci.core.master"
SENT = "active_sentinel"
RT = "runtime"
SET_LINE = "set_line"
REG_GLOB = "register_global"


class TranspilePass(Pass):
    """Jac transpilation to python pass."""

    def __init__(self: "TranspilePass", ir: AstNode) -> None:
        """Initialize pass."""
        super().__init__(ir)

    def exit_int(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""
        node.py_code = str(node.value)

    def exit_float(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""
        node.py_code = str(node.value)

    def exit_multiline(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""

    def exit_bool(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""
        node.py_code = str(node.value)

    def exit_null(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""
        node.py_code = str(node.value)

    def exit_name(self: "TranspilePass", node: AstNode) -> None:
        """Run on INT terminal."""
        node.py_code = str(node.value)
