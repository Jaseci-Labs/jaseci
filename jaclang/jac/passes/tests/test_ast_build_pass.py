"""Test ast build pass module."""
import inspect

from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass
from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa
from jaclang.utils.test import TestCase


class AstBuildPassTests(TestCase):
    """Test pass module."""

    def setUp(self: TestCase) -> None:
        """Set up test."""
        self.lex = JacLexer()
        self.prse = JacParser()
        return super().setUp()

    def test_basic_pass(self: "TestCase") -> None:
        """Basic test for pass."""
        self.lex = JacLexer()
        self.prse = JacParser()
        parse_tree = self.prse.parse(
            self.lex.tokenize(
                self.load_fixture("../../../tests/fixtures/micro/module_structure.jac")
            )
        )
        ast = ptoa(parse_tree)
        build_pass = AstBuildPass(ast)
        print(build_pass.ir.kid[0].kid)
        # self.assertGreater(len(str(build_pass.ir.to_dict())), 1000)

    def parse_micro(self: "AstBuildPass", filename: str) -> None:
        """Parse micro jac file."""
        self.prse.cur_file = filename
        self.prse.parse(self.lex.tokenize(self.load_fixture(f"micro/{filename}")))
        self.assertFalse(self.prse.had_error)

    def test_no_typo_in_pass(self: "TestCase") -> None:
        """Test for enter/exit name diffs with parser."""
        from jaclang.jac.parser import JacParser

        parser_func_names = []
        for name, value in inspect.getmembers(JacParser):
            if (
                inspect.isfunction(value)
                and value.__qualname__.split(".")[0] == JacParser.__name__
            ):
                parser_func_names.append(name)
        ast_build_func_names = []
        for name, value in inspect.getmembers(AstBuildPass):
            if (
                (name.startswith("enter_") or name.startswith("exit_"))
                and inspect.isfunction(value)
                and not getattr(AstBuildPass.__base__, value.__name__, False)
                and value.__qualname__.split(".")[0]
                == AstBuildPass.__name__.replace("enter_", "").replace("exit_", "")
            ):
                ast_build_func_names.append(
                    name.replace("enter_", "").replace("exit_", "")
                )
        for name in ast_build_func_names:
            self.assertIn(name, parser_func_names)

    # def test_pass_grammar_complete(self: "TestCase") -> None:
    #     """Test for enter/exit name diffs with parser."""
    #     from jaclang.jac.parser import JacParser

    #     parser_func_names = []
    #     for name, value in inspect.getmembers(JacParser):
    #         if (
    #             inspect.isfunction(value)
    #             and value.__qualname__.split(".")[0] == JacParser.__name__
    #         ):
    #             parser_func_names.append(name)
    #     ast_build_func_names = []
    #     for name, value in inspect.getmembers(AstBuildPass):
    #         if (
    #             (name.startswith("enter_") or name.startswith("exit_"))
    #             and inspect.isfunction(value)
    #             and not getattr(AstBuildPass.__base__, value.__name__, False)
    #             and value.__qualname__.split(".")[0]
    #             == AstBuildPass.__name__.replace("enter_", "").replace("exit_", "")
    #         ):
    #             ast_build_func_names.append(
    #                 name.replace("enter_", "").replace("exit_", "")
    #             )
    #     for name in parser_func_names:
    #         self.assertIn(name, ast_build_func_names)
