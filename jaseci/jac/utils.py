"""Utility functions and classes for Jac compilation toolchain."""
from typing import Generic, List, TypeVar, Union

from jaseci.utils.sly.lex import Token

T = TypeVar("T")


class Stack(Generic[T]):
    """Stack class for Jac compilation toolchain."""

    def __init__(self: "Stack") -> None:
        """Initialize stack."""
        self.stack: List[T] = []
        self.checkpoint_size = 0

    def push(self: "Stack", item: T) -> None:
        """Push item onto stack."""
        self.stack.append(item)

    def pop(self: "Stack") -> T:
        """Pop item off stack."""
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self: "Stack") -> bool:
        """Check if stack is empty."""
        return len(self.stack) == 0

    def checkpoint(self: "Stack") -> None:
        """Set checkpoint for stack."""
        self.checkpoint_size = len(self.stack)

    def clear_beyond_checkpoint(self: "Stack") -> None:
        """Clear stack beyond checkpoint."""
        if len(self.stack) > self.checkpoint_size:
            del self.stack[self.checkpoint_size :]


def is_term(tree: Union[tuple, Token], specific: str = "") -> bool:
    """Check if tree is terminal."""
    return isinstance(tree, Token) and (tree.type == specific or specific == "")


def term_val(tree: Token) -> str:
    """Return terminal value."""
    return tree.value


def parse_tree_name(tree: Union[tuple, Token]) -> str:
    """Return parse tree name."""
    if isinstance(tree, Token):
        return tree.type
    else:
        return tree[0]
