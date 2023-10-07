"""Lark parser for Jac Lang."""
from __future__ import annotations

import logging
import os

import jaclang.jac.absyntree as ast
from jaclang.jac import jac_lark as jl
from jaclang.jac.passes.ir_pass import Pass
from jaclang.vendor.lark import Lark, logger


class TreeToAST(jl.Transformer):
    """Transform parse tree to AST."""

    def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
        """Initialize transformer."""
        super().__init__(*args, **kwargs)
        self.parse_ref = parser

    def start(self, kid: list[ast.Module]) -> ast.Module:
        """Start."""
        return kid[0]

    def module(self, kid: list[ast.AstNode]) -> ast.AstNode:
        """Builder for Module ast node."""
        doc = kid[0] if len(kid) and isinstance(kid[0], ast.Constant) else None
        body = kid[1:] if doc else kid
        mod = ast.Module(
            name=self.parse_ref.mod_path.split(os.path.sep)[-1].split(".")[0],
            doc=doc,
            body=body,
            mod_path=self.parse_ref.mod_path,
            rel_mod_path=self.parse_ref.rel_mod_path,
            is_imported=False,
            mod_link=None,
        )
        print(mod)
        self.mod_link = mod
        return mod

    def element_with_doc(self, kid: list[ast.AstNode]) -> ast.ElementType:
        """Builder for Elements with docstring ast node."""
        if isinstance(kid[1], ast.ElementType) and isinstance(kid[0], ast.Constant):
            kid[1].doc = kid[0]
            kid[1].add_kid_left(kid[0])
            return kid[1]
        else:
            raise self.ice()

    def element(self, kid: list[ast.AstNode]) -> ast.ElementType:
        """Builder for Element ast nodes."""
        if isinstance(kid[0], ast.ElementType):
            return kid[0]
        else:
            raise self.ice()

    def ice(self) -> Exception:
        """Raise internal compiler error."""
        self.parse_ref.error("Unexpected item in parse tree!")
        return RuntimeError(
            f"{self.parse_ref.__class__.__name__} - Unexpected item in parse tree!"
        )


class JacParser(Pass):
    """Jac Parser."""

    dev_mode = True

    def before_pass(self) -> None:
        """Initialize parser."""
        super().before_pass()
        self.comments = []
        if JacParser.dev_mode:
            JacParser.make_dev()

    def transform(self, ir: ast.SourceString) -> ast.Module:
        """Transform input IR."""
        tree, self.comments = JacParser.parse(ir.value)
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
            strict=True,
            debug=True,
            lexer_callbacks={"COMMENT": JacParser._comment_callback},
        )
        logger.setLevel(logging.DEBUG)

    comment_cache = []
    parser = jl.Lark_StandAlone(lexer_callbacks={"COMMENT": _comment_callback})
