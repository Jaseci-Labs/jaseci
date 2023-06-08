"""Abstract class for IR Passes for Jac."""
from enum import Enum
from pprint import pprint


class AstNodeKind(Enum):
    """Type of node in ast."""

    UNKNOWN = 0
    PARSE_RULE = 1
    TOKEN = 2

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
        misc: dict = None,
    ) -> None:
        """Initialize ast."""
        self.name = name
        self.kind = kind
        self.value = value
        self.kid = kid if kid else []
        self.line = line
        self.py_code = py_code
        self.misc = misc if misc else {}

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
            "misc": self.misc,
        }

    def print(self: "AstNode") -> None:
        """Print ast."""
        pprint(self.to_dict())
