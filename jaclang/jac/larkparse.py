"""Lark parser for Jac Lang."""
import logging
import os
import sys
from typing import Optional

from jaclang.jac.transform import Transform


cur_dir = os.path.dirname(__file__)
if not os.path.exists(os.path.join(cur_dir, "__jac_gen__", "jac_parser.py")):
    from jaclang.vendor.lark.tools import standalone

    os.makedirs(os.path.join(cur_dir, "__jac_gen__"), exist_ok=True)
    with open(os.path.join(cur_dir, "__jac_gen__", "__init__.py"), "w"):
        pass
    save_argv = sys.argv
    sys.argv = [
        "lark",
        os.path.join(cur_dir, "jac.lark"),
        "-o",
        os.path.join(cur_dir, "__jac_gen__", "jac_parser.py"),
        "-c",
    ]
    standalone.main()
    sys.argv = save_argv
from .__jac_gen__.jac_parser import Lark_StandAlone as Lark, logger  # noqa: E402

logger.setLevel(logging.DEBUG)

with open(os.path.join(os.path.dirname(__file__), "jac.lark"), "r") as f:
    jac_grammar = f.read()
comments = []
parser = Lark(
    # strict=True,
    lexer_callbacks={"COMMENT": comments.append},
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

    def transform(self, ir: str) -> Lark:
        """Transform input IR."""
        return parser.parse(ir)
