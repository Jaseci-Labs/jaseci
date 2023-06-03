"""Test pass module."""
from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser
from jaseci.jac.passes.ir_pass import Pass, parse_tree_to_ast as ptoa
from jaseci.utils.test import TestCase


class TestPass(TestCase):
    """Test pass module."""

    def test_basic_pass(self: "TestPass") -> None:
        """Basic test for pass."""
        lexer = JacLexer()
        parser = JacParser()
        parse_tree = parser.parse(lexer.tokenize(self.load_fixture("fam.jac")))
        ast = ptoa(parse_tree)
        self.assertGreater(len(str(Pass(ast).ir.to_dict())), 1000)
