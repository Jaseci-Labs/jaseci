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
        self.builder = AstBuildPass()
        return super().setUp()

    def build_micro(self: "AstBuildPass", filename: str) -> None:
        """Parse micro jac file."""
        self.prse.cur_file = filename
        ptree = self.prse.parse(
            self.lex.tokenize(
                self.load_fixture(f"../../../tests/fixtures/micro/{filename}")
            )
        )
        build_pass = self.builder.run(node=ptoa(ptree))
        return build_pass

    def test_ast_build_basic(self: "TestCase") -> None:
        """Basic test for pass."""
        ptree = self.prse.parse(self.lex.tokenize(self.load_fixture("fam.jac")))
        build_pass = self.builder.run(node=ptoa(ptree))
        build_pass.print()

    def test_ast_build_module_structure(self: "TestCase") -> None:
        """Basic test for pass."""
        build_pass = self.build_micro("module_structure.jac")
        # build_pass.print()
        self.assertGreater(len(str(build_pass.to_dict())), 200)

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

    def test_pass_grammar_complete(self: "TestCase") -> None:
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
        for name in parser_func_names:
            self.assertIn(name, ast_build_func_names)
