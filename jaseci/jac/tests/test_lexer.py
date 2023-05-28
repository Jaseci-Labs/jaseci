"""Tests for Jac lexer."""

from jaseci.jac.lexer import JacLexer
from jaseci.utils.test import TestCase


class TestLexer(TestCase):
    """Test Jac lexer."""

    def setUp(self: "TestLexer") -> None:
        """Set up test case."""
        return super().setUp()

    def tearDown(self: "TestLexer") -> None:
        """Tear down test case."""
        return super().tearDown()

    def test_lexer(self: "TestLexer") -> None:
        """Basic test for lexer."""
        lexer = JacLexer()
        tokens = []
        for t in lexer.tokenize(self.load_fixture("fam.jac")):
            tokens.append(t)
        self.assertEqual(
            [
                tokens[0].type,
                tokens[0].value,
                tokens[0].lineno,
                tokens[0].index,
                tokens[0].end,
            ],
            ["NAME", "node", 1, 0, 4],
        )
        self.assertEqual(
            [
                tokens[10].type,
                tokens[10].value,
                tokens[10].lineno,
                tokens[10].index,
                tokens[10].end,
            ],
            ["NAME", "dad", 5, 38, 41],
        )
        self.assertEqual(
            [
                tokens[-1].type,
                tokens[-1].value,
                tokens[-1].lineno,
                tokens[-1].index,
                tokens[-1].end,
            ],
            ["RBRACE", "}", 22, 407, 408],
        )
