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

    def exit_start(self: "TranspilePass", node: AstNode) -> None:
        """Convert start to python code."""
        node.py_code = node.kid[0].py_code

    def exit_element_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert element list to python code."""
        for i in node.kid:
            node.py_code += i.py_code + "\n"

    def exit_element(self: "TranspilePass", node: AstNode) -> None:
        """Convert element to python code."""
        node.py_code = node.kid[0].py_code

    # def exit_global_var_clause(self: "TranspilePass", node: AstNode) -> None:
    #     """Convert global var clause to python code."""
    #     node.py_code = node.kid[0].py_code

    def exit_global_var(self: "TranspilePass", node: AstNode) -> None:
        """Convert global var to python code."""
        node.py_code = node.kid[1].py_code

    def exit_int(self: "TranspilePass", node: AstNode) -> None:
        """Convert int to python code."""
        node.py_code = str(node.value)

    def exit_float(self: "TranspilePass", node: AstNode) -> None:
        """Convert float to python code."""
        node.py_code = str(node.value)

    def exit_multistring(self: "TranspilePass", node: AstNode) -> None:
        """Convert multistring to python code."""
        for i in node.kid:
            node.py_code += i.py_code + " "
        node.py_code = str(node.value)

    def exit_string(self: "TranspilePass", node: AstNode) -> None:
        """Convert string to python code."""
        node.py_code = str(node.value)

    def exit_doc_string(self: "TranspilePass", node: AstNode) -> None:
        """Convert doc string to python code."""
        node.py_code = str(node.value)

    def exit_bool(self: "TranspilePass", node: AstNode) -> None:
        """Convert bool to python code."""
        node.py_code = str(node.value)

    def exit_null(self: "TranspilePass", node: AstNode) -> None:
        """Convert null to python code."""
        node.py_code = str(node.value)

    def exit_name(self: "TranspilePass", node: AstNode) -> None:
        """Convert name to python code."""
        node.py_code = str(node.value)
