"""Test pass module."""
from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCase


class TestPass(TestCase):
    """Test pass module."""

    def test_basic_pass(self) -> None:
        """Basic test for pass."""
        lexer = JacLexer()
        parser = JacParser()
        parse_tree = parser.parse(
            lexer.tokenize(self.load_fixture("fam.jac")), filename="fam.jac"
        )
        self.assertFalse(parser.had_error)
        ast = ptoa(parse_tree)
        self.assertGreater(len(str(Pass(ir=ast).ir.to_dict())), 1000)

    def test_basic_fstring(self) -> None:
        """Basic test for pass."""
        lexer = JacLexer()
        parser = JacParser()
        parse_tree = parser.parse(
            lexer.tokenize(self.load_fixture("fstrings.jac")), filename="fstrings.jac"
        )
        self.assertFalse(parser.had_error)
        ast = ptoa(parse_tree)
        self.assertGreater(len(str(Pass(ir=ast).ir.to_dict())), 1000)
