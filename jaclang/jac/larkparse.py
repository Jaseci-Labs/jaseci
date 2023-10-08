"""Lark parser for Jac Lang."""
from __future__ import annotations

import logging
import os

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac import jac_lark as jl
from jaclang.jac.passes.ir_pass import Pass
from jaclang.vendor.lark import Lark, logger


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
        tree = JacParser.TreeToAST(parser=self).transform(tree)
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

    class TreeToAST(jl.Transformer):
        """Transform parse tree to AST."""

        def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
            """Initialize transformer."""
            super().__init__(*args, **kwargs)
            self.parse_ref = parser

        def ice(self) -> Exception:
            """Raise internal compiler error."""
            self.parse_ref.error("Unexpected item in parse tree!")
            return RuntimeError(
                f"{self.parse_ref.__class__.__name__} - Unexpected item in parse tree!"
            )

        def start(self, kid: list[ast.Module]) -> ast.Module:
            """
            start: module
            """
            return kid[0]

        def module(self, kid: list[ast.AstNode]) -> ast.AstNode:
            """
            module: (doc_tag? element (element_with_doc | element)*)?
            doc_tag (element_with_doc (element_with_doc | element)*)?
            """
            doc = kid[0] if len(kid) and isinstance(kid[0], ast.Constant) else None
            body = kid[1:] if doc else kid
            valid_body: list[ast.ElementType] = [
                i for i in body if isinstance(i, ast.ElementType)
            ]
            if len(valid_body) == len(body):
                mod = ast.Module(
                    name=self.parse_ref.mod_path.split(os.path.sep)[-1].split(".")[0],
                    doc=doc,
                    body=valid_body,
                    mod_path=self.parse_ref.mod_path,
                    rel_mod_path=self.parse_ref.rel_mod_path,
                    is_imported=False,
                    mod_link=None,
                    kid=kid,
                )
                self.mod_link = mod
                return mod
            else:
                raise self.ice()

        def element_with_doc(self, kid: list[ast.AstNode]) -> ast.ElementType:
            """
            element_with_doc: doc_tag element
            """
            if isinstance(kid[1], ast.ElementType) and isinstance(kid[0], ast.Constant):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                return kid[1]
            else:
                raise self.ice()

        def element(self, kid: list[ast.AstNode]) -> ast.ElementType:
            """
            element: py_code_block
                | include_stmt
                | import_stmt
                | ability
                | architype
                | mod_code
                | test
                | global_var
            """
            if isinstance(kid[0], ast.ElementType):
                return kid[0]
            else:
                raise self.ice()

        def global_var(self, kid: list[ast.AstNode]) -> ast.GlobalVars:
            """
            global_var: (KW_FREEZE | KW_GLOBAL) access_tag? assignment_list SEMI
            """
            is_frozen = isinstance(kid[0], ast.Token) and kid[0].name == Tok.KW_FREEZE
            access = kid[1] if isinstance(kid[1], ast.AccessTag) else None
            assignments = kid[2:-1] if access else kid[1:-1]
            valid_assigns: list[ast.Assignment] = [
                i for i in assignments if isinstance(i, ast.Assignment)
            ]
            if len(valid_assigns) == len(assignments):
                return ast.GlobalVars(
                    access=access,
                    assignments=valid_assigns,
                    is_frozen=is_frozen,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def access_tag(self, kid: list[ast.AstNode]) -> ast.AccessTag:
            """
            access_tag: COLON ( KW_PROT | KW_PUB | KW_PRIV )
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Token):
                return ast.AccessTag(
                    access=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def test(self, kid: list[ast.AstNode]) -> ast.Test:
            """
            test: KW_TEST NAME? code_block
            """
            name = kid[1] if isinstance(kid[1], ast.Name) else kid[0]
            codeblock = kid[2] if name else kid[1]
            if isinstance(codeblock, ast.CodeBlock) and isinstance(
                name, (ast.Name, ast.Token)
            ):
                return ast.Test(
                    name=name,
                    body=codeblock,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def mod_code(self, kid: list[ast.AstNode]) -> ast.ModuleCode:
            """
            mod_code: KW_WITH KW_ENTRY sub_name? code_block
            """
            name = kid[2] if isinstance(kid[2], ast.Name) else None
            codeblock = kid[3] if name else kid[2]
            if isinstance(codeblock, ast.CodeBlock):
                return ast.ModuleCode(
                    name=name,
                    body=codeblock,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()
