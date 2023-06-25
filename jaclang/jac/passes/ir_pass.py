"""Abstract class for IR Passes for Jac."""
import jaclang.jac.absyntree as ast
from jaclang.jac.transform import IRType, Transform
from jaclang.jac.utils import pascal_to_snake


class Pass(Transform):
    """Abstract class for IR passes."""

    def __init__(
        self, mod_path: str, input_ir: ast.AstNode, base_path: str = ""
    ) -> None:
        """Initialize parser."""
        self.cur_node = input_ir  # tracks current node during traversal
        Transform.__init__(self, mod_path, input_ir, base_path)

    def before_pass(self) -> None:
        """Run once before pass."""
        pass

    def after_pass(self) -> None:
        """Run once after pass."""
        pass

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        if hasattr(self, f"enter_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"enter_{pascal_to_snake(type(node).__name__)}")(node)
        if isinstance(node, ast.Parse) and hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        if hasattr(self, f"exit_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"exit_{pascal_to_snake(type(node).__name__)}")(node)
        if isinstance(node, ast.Parse) and hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    # Transform Implementations
    # -------------------------
    def transform(self, ir: IRType) -> IRType:
        """Run pass."""
        self.before_pass()
        if not isinstance(ir, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.traverse(ir)
        self.after_pass()
        # Checks if self.ir is created during traversal
        return self.ir if hasattr(self, "ir") else ir

    def traverse(self, node: ast.AstNode) -> None:
        """Traverse tree."""
        self.cur_node = node
        self.enter_node(node)
        for i in node.kid:
            if i:
                self.traverse(i)
        self.exit_node(node)

    def error(self, msg: str) -> None:
        """Pass Error."""
        if not isinstance(self.cur_node, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.cur_line = self.cur_node.line
        self.log_error(f"{msg}")

    def warning(self, msg: str) -> None:
        """Pass Error."""
        if not isinstance(self.cur_node, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.cur_line = self.cur_node.line
        self.log_error(f"{msg}")


class PrinterPass(Pass):
    """Printer Pass for Jac AST."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        print("Entering:", node)
        super().enter_node(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        super().exit_node(node)
        print("Exiting:", node)
