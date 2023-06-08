"""Abstract class for IR Passes for Jac."""
from jaclang.jac.ast import AstNode, AstNodeKind
from jaclang.utils.sly.lex import Token


class Pass:
    """Abstract class for IR passes."""

    def __init__(self: "Pass", ir: AstNode = None) -> None:
        """Initialize pass."""
        self.ir = ir if ir else AstNode()
        if ir:
            self.run()

    def before_pass(self: "Pass") -> None:
        """Run once before pass."""
        pass

    def after_pass(self: "Pass") -> None:
        """Run once after pass."""
        pass

    def enter_node(self: "Pass", node: AstNode) -> None:
        """Run on entering node."""
        if hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self: "Pass", node: AstNode) -> None:
        """Run on exiting node."""
        if hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def run(self: "Pass") -> AstNode:
        """Run pass."""
        self.before_pass()
        self.traverse()
        self.after_pass()
        return self.ir

    def traverse(self: "Pass", node: AstNode = None) -> None:
        """Traverse tree."""
        if node is None:
            node = self.ir
        self.enter_node(node)
        for i in node.kid:
            self.traverse(i)
        self.exit_node(node)
        self.ir = node  # Makes sure we update the ir with whatever is passed in
        return self.ir


def parse_tree_to_ast(
    tree: tuple, parent: AstNode = None, lineno: int = None
) -> AstNode:
    """Convert parser output to ast, also parses fstrings."""
    from jaclang.utils.fstring_parser import FStringLexer, FStringParser

    if not isinstance(tree, AstNode):
        if isinstance(tree, tuple):
            kids = tree[2:]
            tree = AstNode(
                name=tree[0],
                parent=parent,
                kind=AstNodeKind.PARSE_RULE,
                value="",
                line=tree[1] if lineno is None else lineno,
                py_code="",
            )
            tree.kid = [parse_tree_to_ast(x, parent=tree, lineno=lineno) for x in kids]
        elif isinstance(tree, Token):
            if tree.type == "FSTRING":
                lineno = tree.lineno
                tree = FStringParser().parse(FStringLexer().tokenize(tree.value))
                return parse_tree_to_ast(tree, parent=parent, lineno=lineno)
            else:
                tree = AstNode(
                    name=tree.type,
                    parent=parent,
                    kind=AstNodeKind.TOKEN,
                    value=tree.value,
                    kid=[],
                    line=tree.lineno if lineno is None else lineno,
                    py_code="",
                )
        else:
            raise ValueError(f"node must be AstNode or parser output tuple: {tree}")
    return tree
