"""Abstract class for IR Passes for Jac."""
import jaclang.jac.ast as ast
from jaclang.jac.utils import pascal_to_snake
from jaclang.utils.sly.lex import Token


class Pass:
    """Abstract class for IR passes."""

    def __init__(self: "Pass", ir: ast.AstNode = None) -> None:
        """Initialize pass."""
        self.ir = ir if ir else ast.AstNode(parent=None, kid=[], line=0)
        if ir:
            self.run()

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

    def run(self: "Pass", node: ast.AstNode = None) -> ast.AstNode:
        """Run pass."""
        if node is None:
            node = self.ir
        self.before_pass()
        self.traverse(node)
        self.after_pass()
        return self.ir

    def traverse(self: "Pass", node: ast.AstNode) -> None:
        """Traverse tree."""
        self.enter_node(node)
        for i in node.kid:
            self.traverse(i)
        self.exit_node(node)


def parse_tree_to_ast(
    tree: tuple, parent: ast.AstNode = None, lineno: int = None
) -> ast.AstNode:
    """Convert parser output to ast, also parses fstrings."""
    from jaclang.utils.fstring_parser import FStringLexer, FStringParser

    if not isinstance(tree, ast.AstNode):
        if isinstance(tree, tuple):
            kids = tree[2:]
            tree = ast.Parse(
                name=tree[0],
                parent=parent,
                line=tree[1] if lineno is None else lineno,
                kid=[],
            )
            tree.kid = [parse_tree_to_ast(x, parent=tree, lineno=lineno) for x in kids]
        elif isinstance(tree, Token):
            if tree.type == "FSTRING":
                lineno = tree.lineno
                tree = FStringParser().parse(FStringLexer().tokenize(tree.value))
                return parse_tree_to_ast(tree, parent=parent, lineno=lineno)
            else:
                tree = ast.Token(
                    name=tree.type,
                    parent=parent,
                    value=tree.value,
                    kid=[],
                    line=tree.lineno if lineno is None else lineno,
                )
        else:
            raise ValueError(f"node must be ast.AstNode or parser output tuple: {tree}")
    return tree
