"""Lark parser for Jac Lang."""
import os
from typing import Optional

from jaclang.jac.transform import Transform
from jaclang.vendor.lark import Lark, ParseTree


with open(os.path.join(os.path.dirname(__file__), "jac.lark"), "r") as f:
    jac_grammar = f.read()


class JacParser(Transform):
    """Jac Parser."""

    def __init__(
        self,
        mod_path: str,
        input_ir: str,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize parser."""
        self.comments = []
        self.parser = Lark(
            jac_grammar,
            parser="lalr",
            lexer_callbacks={"COMMENT": self.comments.append},
        )
        self.ir = self.transform(input_ir)

    def transform(self, ir: str) -> ParseTree:
        """Transform input IR."""
        return self.parser.parse(ir)
