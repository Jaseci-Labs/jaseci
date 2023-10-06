"""Lark parser for Jac Lang."""
import logging
from typing import Optional

from jaclang.jac import JacLark, Transformer
from jaclang.jac.transform import Transform
from jaclang.vendor.lark import Lark, ParseTree, logger


class TreeToAST(Transformer):
    """Transform parse tree to AST."""

    def start(self, children: list[ParseTree]) -> list[ParseTree]:
        """Start."""
        print(children)
        return children


class JacParser(Transform):
    """Jac Parser."""

    dev_mode = False

    def __init__(
        self,
        mod_path: str,
        input_ir: str,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize parser."""
        self.comments = []
        if JacParser.dev_mode:
            JacParser.make_dev()
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

    @staticmethod
    def make_dev() -> None:
        """Make parser in dev mode."""
        JacParser.parser = Lark.open(
            "jac.lark",
            parser="lalr",
            rel_to=__file__,
            debug=True,
            lexer_callbacks={"COMMENT": JacParser._comment_callback},
        )
        logger.setLevel(logging.DEBUG)

    comment_cache = []
    parser = JacLark(
        transformer=TreeToAST(), lexer_callbacks={"COMMENT": _comment_callback}
    )
    # parser = JacLark(lexer_callbacks={"COMMENT": _comment_callback})
