"""Abstract class for IR Passes for Jac."""
from typing import Optional, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.transform import Transform
from jaclang.utils.helpers import pascal_to_snake

T = TypeVar("T", bound=ast.AstNode)


class Pass(Transform):
    """Abstract class for IR passes."""

    def __init__(
        self,
        prior: Transform,
        mod_path: str,
        input_ir: ast.AstNode,
        base_path: str = "",
    ) -> None:
        """Initialize parser."""
        self.term_signal = False
        self.prune_signal = False
        self.cur_node = input_ir  # tracks current node during traversal
        self.ir = input_ir
        Transform.__init__(self, mod_path, input_ir, base_path, prior)

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

    def terminate(self) -> None:
        """Terminate traversal."""
        self.term_signal = True

    def prune(self) -> None:
        """Prune traversal."""
        self.prune_signal = True

    def get_all_sub_nodes(
        self, node: ast.AstNode, typ: type[T], brute_force: bool = False
    ) -> list[T]:
        """Get all sub nodes of type."""
        result = []
        # Assumes pass built the sub node table
        if not node:
            return result
        elif len(node._sub_node_tab) and not brute_force:
            result.extend(node._sub_node_tab[typ] if typ in node._sub_node_tab else [])
        elif len(node.kid):
            if not brute_force:
                raise ValueError(f"Node has no sub_node_tab. {node}")
            # Brute force search
            else:
                for i in node.kid:
                    if isinstance(i, typ):
                        result.append(i)
                    result.extend(self.get_all_sub_nodes(i, typ, brute_force))
        return result

    def recalculate_parents(self, node: ast.AstNode) -> None:
        """Recalculate parents."""
        if not node:
            return
        for i in node.kid:
            if i:
                i.parent = node
                self.recalculate_parents(i)

    # Transform Implementations
    # -------------------------
    def transform(self, ir: ast.AstNode) -> ast.AstNode:
        """Run pass."""
        # Only performs passes on proper ASTs
        if not isinstance(ir, ast.AstNode):
            return ir
        self.before_pass()
        if not isinstance(ir, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.traverse(ir)
        # Checks if self.ir is created during traversal
        self.ir = self.ir if hasattr(self, "ir") else ir
        self.after_pass()
        return self.ir

    def traverse(self, node: ast.AstNode) -> ast.AstNode:
        """Traverse tree."""
        if self.term_signal:
            return node
        self.cur_node = node
        self.enter_node(node)
        if not self.prune_signal:
            for i in node.kid:
                if i:
                    self.traverse(i)
        else:
            self.prune_signal = False
        self.cur_node = node
        self.exit_node(node)
        return node

    def update_code_loc(self, node: Optional[ast.AstNode] = None) -> None:
        """Update code location."""
        if node is None:
            node = self.cur_node
        if not isinstance(node, ast.AstNode):
            self.ice("Current node is not an AstNode.")
        self.cur_line = node.line
        if node.mod_link:
            self.rel_mod_path = node.mod_link.rel_mod_path
            self.mod_path = node.mod_link.mod_path

    def error(self, msg: str, node_override: Optional[ast.AstNode] = None) -> None:
        """Pass Error."""
        self.update_code_loc(node_override)
        self.log_error(f"{msg}")

    def warning(self, msg: str, node_override: Optional[ast.AstNode] = None) -> None:
        """Pass Error."""
        self.update_code_loc(node_override)
        self.log_warning(f"{msg}")

    def ice(self, msg: str = "Something went horribly wrong!") -> None:
        """Pass Error."""
        if isinstance(self.cur_node, ast.AstNode):
            self.cur_line = self.cur_node.line
        self.log_error(f"ICE: Pass {self.__class__.__name__} - {msg}")
        raise RuntimeError(
            f"Internal Compiler Error: Pass {self.__class__.__name__} - {msg}"
        )


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
