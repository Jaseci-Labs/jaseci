"""Lark parser for Jac Lang."""
from __future__ import annotations

import logging
import os
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac import jac_lark as jl
from jaclang.jac.transform import Transform
from jaclang.vendor.lark import Lark, logger


class TreeToAST(jl.Transformer):
    """Transform parse tree to AST."""

    def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
        """Initialize transformer."""
        super().__init__(*args, **kwargs)
        self.parser = parser

    def start(self, kid: list[ast.Module]) -> ast.Module:
        """Start."""
        return kid[0]

    def module(self, kid: list[ast.AstNode]) -> ast.Module:
        """Builder for Module ast node."""
        doc = kid[0] if len(kid) and isinstance(kid[0], ast.Constant) else None
        body = kid[1:] if doc else kid
        return ast.Module(
            name=self.parser.mod_path.split(os.path.sep)[-1].split(".")[0],
            doc=doc,
            body=body,
            mod_path=self.parser.mod_path,
            rel_mod_path=self.parser.rel_mod_path,
            is_imported=False,
            parent=None,
            mod_link=None,
        )


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

    def transform(self, ir: str) -> ast.Module:
        """Transform input IR."""
        tree, self.comments = JacParser.parse(ir)
        tree = TreeToAST(parser=self).transform(tree)
        return tree

    @staticmethod
    def _comment_callback(comment: str) -> None:
        JacParser.comment_cache.append(comment)

    @staticmethod
    def parse(ir: str) -> tuple[jl.Tree, list[str]]:
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
    parser = jl.Lark_StandAlone(lexer_callbacks={"COMMENT": _comment_callback})
