"""Test transpiler."""
import inspect

from jaseci.jac.transpile import JacTranspiler
from jaseci.utils.test import TestCase


class TestTranspiler(TestCase):
    """Test Jac transpiler."""

    def test_core_transpiler_loop(self: "TestTranspiler") -> None:
        """Basic test for transpiler."""
        transpiler = JacTranspiler()
        output = transpiler.transpile(self.load_fixture("fam.jac"))
        print(output)
        self.assertIsNotNone(output)

    def test_transpiler_parser_rules_match(self: "TestTranspiler") -> None:
        """Test number and names of transpiler and parser rules match."""
        from jaseci.jac.parser import JacParser

        parser_func_names = [
            attr
            for attr in dir(JacParser)
            if inspect.isfunction(getattr(JacParser, attr))
        ]

        transpiler_func_names = [
            attr
            for attr in dir(JacTranspiler)
            if inspect.isfunction(getattr(JacTranspiler, attr))
            and attr.startswith("transpile_")
        ]

        parser_only_funcs = [
            x
            for x in parser_func_names
            if "transpile_" + x not in transpiler_func_names
        ]

        self.assertEqual(len(parser_func_names) - 6, len(transpiler_func_names))
        self.assertEqual(
            parser_only_funcs,
            ["errok", "error", "index_position", "line_position", "parse", "restart"],
        )
