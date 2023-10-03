"""Test ast build pass module."""
import inspect

from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.blue import AstBuildPass
from jaclang.utils.fstring_parser import FStringParser
from jaclang.utils.test import TestCaseMicroSuite


class AstBuildPassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pass_grammar_complete(self) -> None:
        """Test for enter/exit name diffs with parser."""
        from jaclang.jac.parser import JacParser

        parser_func_names = []
        for name, value in [
            *inspect.getmembers(JacParser),
            *inspect.getmembers(FStringParser),
        ]:
            if (
                inspect.isfunction(value)
                and value.__qualname__.split(".")[0]
                in [JacParser.__name__, FStringParser.__name__]
                and name not in ["__init__", "error", "transform"]
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
        for name in parser_func_names:
            self.assertIn(name, ast_build_func_names)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        lex = JacLexer(mod_path=f"{filename}", input_ir=self.file_to_str(filename)).ir
        prse = JacParser(mod_path=f"{filename}", input_ir=lex)
        build_pass = AstBuildPass(mod_path="", prior=prse, input_ir=prse.ir).ir
        self.assertIsNotNone(build_pass)
        if build_pass:
            self.assertGreater(len(str(build_pass.to_dict())), 200)


AstBuildPassTests.self_attach_micro_tests()
