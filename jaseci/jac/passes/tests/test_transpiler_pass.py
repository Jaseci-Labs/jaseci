"""Transpiler pass module."""
import inspect

from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser
from jaseci.jac.passes.ir_pass import parse_tree_to_ast as ptoa
from jaseci.jac.passes.transpiler_pass import TranspilePass
from jaseci.utils.test import TestCase


class TranspilerPassTests(TestCase):
    """Test pass module."""

    def test_basic_pass(self: "TestCase") -> None:
        """Basic test for pass."""
        lexer = JacLexer()
        parser = JacParser()
        parse_tree = parser.parse(lexer.tokenize(self.load_fixture("fam.jac")))
        ast = ptoa(parse_tree)
        self.assertGreater(len(str(TranspilePass(ast).ir.to_dict())), 1000)

    def test_no_typo_in_pass(self: "TestCase") -> None:
        """Test for enter/exit name diffs with parser."""
        from jaseci.jac.parser import JacParser

        parser_func_names = [x.lower() for x in JacParser.tokens]
        for name, value in inspect.getmembers(JacParser):
            if (
                inspect.isfunction(value)
                and value.__qualname__.split(".")[0] == JacParser.__name__
            ):
                parser_func_names.append(name)
        transpile_func_names = []
        for name, value in inspect.getmembers(TranspilePass):
            if (
                (name.startswith("enter_") or name.startswith("exit_"))
                and inspect.isfunction(value)
                and value.__qualname__.split(".")[0]
                == TranspilePass.__name__.replace("enter_", "").replace("exit_", "")
            ):
                transpile_func_names.append(
                    name.replace("enter_", "").replace("exit_", "")
                )
        for name in transpile_func_names:
            self.assertIn(name, parser_func_names)
