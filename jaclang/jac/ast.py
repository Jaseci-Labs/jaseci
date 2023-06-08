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
        name: str = "",
        kind: AstNodeKind = AstNodeKind.UNKNOWN,
        value: str = "",
        kid: list = None,
        line: int = 0,
        py_code: str = "",
        meta: dict = None,
    ) -> None:
        """Initialize ast."""
        self.name = name
        self.kind = kind
        self.value = value
        self.kid = kid if kid else []
        self.line = line
        self.py_code = py_code
        self.meta = meta if meta else {}

    def __str__(self: "AstNode") -> str:
        """Return string representation of node."""
        return (
            f"{self.name} {self.line}, ({self.value}), "
            f"{len(self.kid)} kids, {str(self.kind)}"
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
            "py_code": self.py_code,
            "misc": self.meta,
        }

    def print(self: "AstNode", depth: int = 0) -> None:
        """Print ast."""
        pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())
