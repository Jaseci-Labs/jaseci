"""Abstract class for IR Passes for Jac."""
from typing import Callable, List, Optional, Type

import jaclang.jac.jac_ast as ast
from jaclang.jac.utils import pascal_to_snake
from jaclang.utils.log import logging
from jaclang.utils.sly import lex


class Pass:
    """Abstract class for IR passes."""

    marked_incomplete: List[str] = []

    def __init__(self: "Pass", ir: Optional[ast.AstNode] = None) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
        self.ir = ir if ir else ast.AstNode(parent=ir, kid=[], line=0)
        self.cur_node = ir  # tracks current node during traversal
        self.run()

    @classmethod
    def incomplete(cls: Type["Pass"], func: Callable) -> Callable:
        """Mark function as incomplete, used as indicator for future passes."""
        cls.marked_incomplete.append(func.__name__)

        def wrapper(*args: list, **kwargs: dict) -> None:
            return func(*args, **kwargs)

        return wrapper

    def before_pass(self: "Pass") -> None:
        """Run once before pass."""
        pass

    def after_pass(self: "Pass") -> None:
        """Run once after pass."""
        pass

    def enter_node(self: "Pass", node: ast.AstNode) -> None:
        """Run on entering node."""
        if isinstance(node, ast.Parse):
            if hasattr(self, f"enter_{node.name}"):
                getattr(self, f"enter_{node.name}")(node)
        elif hasattr(self, f"enter_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"enter_{pascal_to_snake(type(node).__name__)}")(node)

    def exit_node(self: "Pass", node: ast.AstNode) -> None:
        """Run on exiting node."""
        if isinstance(node, ast.Parse):
            if hasattr(self, f"exit_{node.name}"):
                getattr(self, f"exit_{node.name}")(node)
        elif hasattr(self, f"exit_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"exit_{pascal_to_snake(type(node).__name__)}")(node)

    def run(self: "Pass", node: Optional[ast.AstNode] = None) -> ast.AstNode:
        """Run pass."""
        if node is None:
            node = self.ir
        self.before_pass()
        self.traverse(node)
        self.after_pass()
        return self.ir

    def traverse(self: "Pass", node: ast.AstNode) -> None:
        """Traverse tree."""
        self.cur_node = node
        self.enter_node(node)
        for i in node.kid:
            if i:
                self.traverse(i)
        self.exit_node(node)

    def get_imcomplete(self: "Pass") -> List[str]:
        """Return list of incomplete functions."""
        return self.marked_incomplete

    def error(self, msg: str) -> None:
        """Pass Error."""
        if self.cur_node:
            self.logger.error(f"Line {self.cur_node.line}, " + msg)

    def warning(self, msg: str) -> None:
        """Pass Error."""
        if self.cur_node:
            self.logger.warning(f"Line {self.cur_node.line}, " + msg)


def parse_tree_to_ast(
    tree: tuple, parent: Optional[ast.AstNode] = None, lineno: int = 0
) -> ast.AstNode:
    """Convert parser output to ast, also parses fstrings."""
    from jaclang.utils.fstring_parser import FStringLexer, FStringParser

    ast_tree: Optional[ast.AstNode] = None
    if not isinstance(tree, ast.AstNode):
        if isinstance(tree, tuple):
            kids = tree[2:]
            ast_tree = ast.Parse(
                name=tree[0],
                parent=parent,
                line=tree[1] if lineno is None else lineno,
                kid=[],
            )
            ast_tree.kid = [
                parse_tree_to_ast(x, parent=ast_tree, lineno=lineno) for x in kids
            ]
        elif isinstance(tree, lex.Token):
            if tree.type == "FSTRING":
                lineno = tree.lineno
                tree = FStringParser().parse(FStringLexer().tokenize(tree.value))
                return parse_tree_to_ast(tree, parent=parent, lineno=lineno)
            else:
                ast_tree = ast.Token(
                    name=tree.type,
                    parent=parent,
                    value=tree.value,
                    kid=[],
                    line=tree.lineno if lineno is None else lineno,
                )
        else:
            raise ValueError(f"node must be ast.AstNode or parser output tuple: {tree}")
    return ast_tree
