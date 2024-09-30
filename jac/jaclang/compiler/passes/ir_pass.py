"""Abstract class for IR Passes for Jac."""

import time
from typing import Optional, Type, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes.transform import Transform
from jaclang.settings import settings
from jaclang.utils.helpers import pascal_to_snake

T = TypeVar("T", bound=ast.AstNode)


class Pass(Transform[T]):
    """Abstract class for IR passes."""

    def __init__(self, input_ir: T, prior: Optional[Transform]) -> None:
        """Initialize parser."""
        self.term_signal = False
        self.prune_signal = False
        self.ir: ast.AstNode = input_ir
        self.time_taken = 0.0
        Transform.__init__(self, input_ir, prior)

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

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        if hasattr(self, f"exit_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"exit_{pascal_to_snake(type(node).__name__)}")(node)

    def terminate(self) -> None:
        """Terminate traversal."""
        self.term_signal = True

    def prune(self) -> None:
        """Prune traversal."""
        self.prune_signal = True

    @staticmethod
    def get_all_sub_nodes(
        node: ast.AstNode, typ: Type[T], brute_force: bool = False
    ) -> list[T]:
        """Get all sub nodes of type."""
        result: list[T] = []
        # Assumes pass built the sub node table
        if not node:
            return result
        elif len(node._sub_node_tab):
            if typ in node._sub_node_tab:
                for i in node._sub_node_tab[typ]:
                    if isinstance(i, typ):
                        result.append(i)
        elif len(node.kid):
            if not brute_force:
                raise ValueError(f"Node has no sub_node_tab. {node}")
            # Brute force search
            else:
                for i in node.kid:
                    if isinstance(i, typ):
                        result.append(i)
                    result.extend(Pass.get_all_sub_nodes(i, typ, brute_force))
        return result

    @staticmethod
    def find_parent_of_type(node: ast.AstNode, typ: Type[T]) -> Optional[T]:
        """Check if node has parent of type."""
        while node.parent:
            if isinstance(node.parent, typ):
                return node.parent
            node = node.parent
        return None

    @staticmethod
    def has_parent_of_node(node: ast.AstNode, parent: ast.AstNode) -> bool:
        """Check if node has parent of type."""
        while node.parent:
            if node.parent == parent:
                return True
            node = node.parent
        return False

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
    def transform(self, ir: T) -> ast.AstNode:
        """Run pass."""
        # Only performs passes on proper ASTs
        if not isinstance(ir, ast.AstNode):
            return ir
        start_time = time.time()
        self.before_pass()
        if not isinstance(ir, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.traverse(ir)
        self.after_pass()
        self.time_taken = time.time() - start_time
        if settings.pass_timer:
            self.log_info(
                f"Time taken in {self.__class__.__name__}: {self.time_taken:.4f} seconds"
            )
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
        if self.term_signal:
            return node
        self.exit_node(node)
        return node

    def error(self, msg: str, node_override: Optional[ast.AstNode] = None) -> None:
        """Pass Error."""
        self.log_error(msg, node_override=node_override)

    def warning(self, msg: str, node_override: Optional[ast.AstNode] = None) -> None:
        """Pass Error."""
        self.log_warning(msg, node_override=node_override)

    def ice(self, msg: str = "Something went horribly wrong!") -> RuntimeError:
        """Pass Error."""
        self.log_error(f"ICE: Pass {self.__class__.__name__} - {msg}")
        return RuntimeError(
            f"Internal Compiler Error: Pass {self.__class__.__name__} - {msg}"
        )


class PrinterPass(Pass):
    """Printer Pass for Jac AST."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        self.log_info(f"Entering: {node.__class__.__name__}: {node.loc}")
        super().enter_node(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        super().exit_node(node)
        self.log_info(f"Exiting: {node.__class__.__name__}: {node.loc}")
