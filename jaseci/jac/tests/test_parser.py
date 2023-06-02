"""Tests for Jac parser."""

from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser
from jaseci.utils.test import TestCase


class TestParser(TestCase):
    """Test Jac parser."""

    def test_parser(self: "TestParser") -> None:
        """Basic test for lexer."""
        lexer = JacLexer()
        parser = JacParser()
        output = parser.parse(lexer.tokenize(self.load_fixture("stuff.jac")))
        print(output)
        self.assertGreater(len(str(output)), 1000)
