"""Tests for Jac parser."""

from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser
from jaseci.jac.tests.fixtures import treedump
from jaseci.utils.test import TestCase


class TestParser(TestCase):
    """Test Jac parser."""

    def test_parser(self: "TestParser") -> None:
        """Basic test for lexer."""
        lexer = JacLexer()
        parser = JacParser()
        tokens = []
        for i in lexer.tokenize(self.load_fixture("fam.jac")):
            tokens.append(i)
        output = parser.parse(lexer.tokenize(self.load_fixture("fam.jac")))
        self.assertEqual(output, treedump.tree)
