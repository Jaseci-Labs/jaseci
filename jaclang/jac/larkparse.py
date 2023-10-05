"""Lark parser for Jac Lang."""

from typing import Optional

from jaclang.jac import JacLark
from jaclang.jac.transform import Transform
from jaclang.vendor.lark import ParseTree


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
        tree, self.comments = JacParser.parse(ir)
        return tree

    @staticmethod
    def _comment_callback(comment: str) -> None:
        JacParser.comment_cache.append(comment)

    @staticmethod
    def parse(ir: str) -> tuple[ParseTree, list[str]]:
        """Parse input IR."""
        JacParser.comment_cache = []
        return (
            JacParser.parser.parse(ir),
            JacParser.comment_cache,
        )

    comment_cache = []
    parser = JacLark(lexer_callbacks={"COMMENT": _comment_callback})
