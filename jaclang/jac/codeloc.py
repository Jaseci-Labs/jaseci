"""Code location info for AST nodes."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jaclang.jac.absyntree import Token


class CodeLocInfo:
    """Code location info."""

    def __init__(
        self,
        first_tok: Token,
        last_tok: Token,
    ) -> None:
        """Initialize code location info."""
        self.first_tok = first_tok
        self.last_tok = last_tok

    @property
    def first_line(self) -> int:
        """Get line number."""
        return self.first_tok.line_no

    @property
    def last_line(self) -> int:
        """Get line number."""
        return self.last_tok.line_no

    @property
    def col_start(self) -> int:
        """Get column position number."""
        return self.first_tok.c_start

    @property
    def col_end(self) -> int:
        """Get column position number."""
        return self.last_tok.c_end

    @property
    def pos_start(self) -> int:
        """Get column position number."""
        return self.first_tok.pos_start

    @property
    def pos_end(self) -> int:
        """Get column position number."""
        return self.last_tok.pos_end

    @property
    def tok_range(self) -> tuple[Token, Token]:
        """Get token range."""
        return (self.first_tok, self.last_tok)

    @property
    def first_token(self) -> Token:
        """Get first token."""
        return self.first_tok

    @property
    def last_token(self) -> Token:
        """Get last token."""
        return self.last_tok

    def update_token_range(self, first_tok: Token, last_tok: Token) -> None:
        """Update token range."""
        self.first_tok = first_tok
        self.last_tok = last_tok

    def update_first_token(self, first_tok: Token) -> None:
        """Update first token."""
        self.first_tok = first_tok

    def update_last_token(self, last_tok: Token) -> None:
        """Update last token."""
        self.last_tok = last_tok
