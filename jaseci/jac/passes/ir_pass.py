"""Abstract class for IR Passes for Jac."""
from enum import Enum

from jaseci.utils.sly.lex import Token


class AstNodeKind(Enum):
    """Type of node in ast."""

    UNKNOWN = 0
    PARSE_RULE = 1
    TOKEN = 2

    def __repr__(self: "AstNodeKind") -> str:
        """Return string representation of AstNodeKind."""
        return self.name


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(
        self: "AstNode",
        name: str = "",
        kind: AstNodeKind = AstNodeKind.UNKNOWN,
        value: str = "",
        kid: list = None,
        line: int = 0,
        py_code: str = "",
    ) -> None:
        """Initialize ast."""
        self.name = name
        self.kind = kind
        self.value = value
        self.kid = kid if kid else []
        self.line = line
        self.py_code = py_code

    def to_dict(self: "AstNode") -> dict:
        """Return dict representation of node."""
        return {
            "name": self.name,
            "kind": self.kind,
            "value": self.value,
            "kid": [x.to_dict() for x in self.kid],
            "line": self.line,
            "py_code": self.py_code,
        }


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
        pass

    def exit_node(self: "Pass", node: AstNode) -> None:
        """Run on exiting node."""
        pass

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


def parse_tree_to_ast(tree: tuple) -> AstNode:
    """Convert parser output to ast."""
    if not isinstance(tree, AstNode):
        if isinstance(tree, tuple):
            tree = AstNode(
                name=tree[0],
                kind=AstNodeKind.PARSE_RULE,
                value="",
                kid=[parse_tree_to_ast(x) for x in tree[2:]],
                line=tree[1],
                py_code="",
            )
        elif isinstance(tree, Token):
            tree = AstNode(
                name=tree.type,
                kind=AstNodeKind.TOKEN,
                kid=[],
                line=tree.lineno,
                py_code="",
            )
        else:
            raise ValueError("node must be AstNode or parser output tuple")
    return tree
