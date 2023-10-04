"""Lark parser for Jac Lang."""
import logging
import os
from typing import Optional

from jaclang.jac.transform import Transform
from jaclang.vendor.lark import Lark, ParseTree, logger

logger.setLevel(logging.DEBUG)


with open(os.path.join(os.path.dirname(__file__), "jac.lark"), "r") as f:
    jac_grammar = f.read()
parser = Lark(
    jac_grammar,
    parser="lalr",
    # strict=True,
    # debug=True,
    # lexer_callbacks={"COMMENT": self.comments.append},
)


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

        Transform.__init__(self, mod_path, input_ir, base_path, prior)

    def transform(self, ir: str) -> ParseTree:
        """Transform input IR."""
        return parser.parse(ir)
