"""Lark parser for Jac Lang."""
import logging
import os
from typing import Optional

from jaclang.jac.transform import Transform
from jaclang.vendor.lark import Lark, ParseTree, logger

logger.setLevel(logging.DEBUG)

# cur_dir = os.path.dirname(__file__)
# if not os.path.exists(os.path.join(cur_dir, "__jac_gen__", "jac.lark")):
#     from jaclang.vendor.lark.tools import standalone

#     os.mkdir(os.path.join(cur_dir, "__jac_gen__"))
#     args = [
#         os.path.join(cur_dir, "jac.lark"),
#         "-o",
#         os.path.join(cur_dir, "__jac_gen__", "jac_parser.py"),
#     ]
#     standalone.main(args)


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
