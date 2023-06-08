"""Abstract class for IR Passes for Jac."""
import pprint
from enum import Enum, auto


class AstNodeKind(Enum):
    """Type of node in ast."""

    UNKNOWN = auto()
    PARSE_RULE = auto()
    TOKEN = auto()
    WHOLE_BUILD = auto()
    DOC_STRING = auto()
    GLOBAL_VAR = auto()
    NAMED_ASSIGN = auto()
    TEST = auto()
    IMPORT = auto()
    IMPORT_FROM = auto()

    def __str__(self: "AstNodeKind") -> str:
        """Return string representation of AstNodeKind."""
        return self.name

    def __repr__(self: "AstNodeKind") -> str:
        """Return string representation of AstNodeKind."""
        return str(self)


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(
        self: "AstNode",
        parent: "AstNode" = None,
        name: str = "",
        kind: AstNodeKind = AstNodeKind.UNKNOWN,
        value: str = "",
        kid: list = None,
        line: int = 0,
        meta: dict = None,
    ) -> None:
        """Initialize ast."""
        self.name = name
        self.parent = parent
        self.kind = kind
        self.value = value
        self.kid = kid if kid else []
        self.line = line
        self.meta = meta if meta else {}

    def __str__(self: "AstNode") -> str:
        """Return string representation of node."""
        return (
            f"{str(self.kind)}->[{self.line},{self.name},({self.value}),"
            f"{len(self.kid)} kids]"
        )

    def __repr__(self: "AstNode") -> str:
        """Return string representation of node."""
        return str(self)

    def to_dict(self: "AstNode") -> dict:
        """Return dict representation of node."""
        return {
            "name": self.name,
            "kind": self.kind,
            "value": self.value,
            "kid": [x.to_dict() for x in self.kid],
            "line": self.line,
            "misc": self.meta,
        }

    def print(self: "AstNode", depth: int = 0) -> None:
        """Print ast."""
        pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())
