"""Abstract class for IR Passes for Jac."""
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.utils import pascal_to_snake
from jaclang.utils.log import logging
from jaclang.utils.sly import lex


class Pass:
    """Abstract class for IR passes."""

    def __init__(self, mod_name: str = "", ir: Optional[ast.AstNode] = None) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
        self.ir = ir if ir else ast.AstNode(parent=ir, kid=[], line=0)
        self.cur_node = ir  # tracks current node during traversal
        self.mod_name = mod_name
        self.run()

    def before_pass(self) -> None:
        """Run once before pass."""
        pass

    def after_pass(self) -> None:
        """Run once after pass."""
        pass

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        if isinstance(node, ast.Parse):
            if hasattr(self, f"enter_{node.name}"):
                getattr(self, f"enter_{node.name}")(node)
        elif hasattr(self, f"enter_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"enter_{pascal_to_snake(type(node).__name__)}")(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        if type(node).__name__ == "KVPair":
            print(pascal_to_snake(type(node).__name__))
        if isinstance(node, ast.Parse):
            if hasattr(self, f"exit_{node.name}"):
                getattr(self, f"exit_{node.name}")(node)
        elif hasattr(self, f"exit_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"exit_{pascal_to_snake(type(node).__name__)}")(node)

    def run(self, node: Optional[ast.AstNode] = None) -> ast.AstNode:
        """Run pass."""
        if node is None:
            node = self.ir
        self.before_pass()
        self.traverse(node)
        self.after_pass()
        return self.ir

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
        if self.cur_node:
            self.logger.error(f"Mod {self.mod_name}, Line {self.cur_node.line}, " + msg)

    def warning(self, msg: str) -> None:
        """Pass Error."""
        if self.cur_node:
            self.logger.warning(
                f"Mod {self.mod_name}, Line {self.cur_node.line}, " + msg
            )


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
                line=tree[1] if lineno == 0 else lineno,
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
                    line=tree.lineno if lineno == 0 else lineno,
                    col_start=tree.index - tree.lineidx + 1,
                    col_end=tree.end - tree.lineidx + 1,
                )
        else:
            raise ValueError(f"node must be ast.AstNode or parser output tuple: {tree}")
    if not ast_tree:
        raise ValueError(f"node must be ast.AstNode: {tree}")
    return ast_tree
