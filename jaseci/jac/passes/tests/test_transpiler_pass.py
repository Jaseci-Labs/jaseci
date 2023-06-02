"""Transpiler pass module."""
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
