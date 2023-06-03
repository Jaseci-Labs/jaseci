"""Test transpiler."""
# import inspect

# from jaseci.jac.transpile import JacTranspiler
from jaseci.utils.test import TestCase


class TestTranspiler(TestCase):
    """Test Jac transpiler."""

    # def test_core_transpiler_loop(self: "TestTranspiler") -> None:
    #     """Basic test for transpiler."""
    #     transpiler = JacTranspiler()
    #     output = transpiler.transpile(self.load_fixture("fam.jac"))
    #     self.assertIsNotNone(output)

    # def test_transpiler_parser_rules_match(self: "TestTranspiler") -> None:
    #     """Test number and names of transpiler and parser rules match."""
    #     from jaseci.jac.parser import JacParser

    #     parser_func_names = []
    #     for name, value in inspect.getmembers(JacParser):
    #         if (
    #             inspect.isfunction(value)
    #             and value.__qualname__.split(".")[0] == JacParser.__name__
    #         ):
    #             parser_func_names.append(name)

    #     transpiler_func_names = []
    #     for name, value in inspect.getmembers(JacTranspiler):
    #         if (
    #             name.startswith("transpile_")
    #             and inspect.isfunction(value)
    #             and value.__qualname__.split(".")[0] == JacTranspiler.__name__
    #         ):
    #             transpiler_func_names.append(name.replace("transpile_", ""))

    #     self.assertEqual(len(parser_func_names), len(transpiler_func_names))
