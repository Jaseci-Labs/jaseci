"""Tests for Jac lexer."""

from jaclang.jac.lexer import JacLexer
from jaclang.utils.test import TestCase


class TestLexer(TestCase):
    """Test Jac lexer."""

    def test_lexer(self) -> None:
        """Basic test for lexer."""
        lexer = JacLexer()
        tokens = []
        for t in lexer.tokenize(self.load_fixture("lexer_fam.jac")):
            tokens.append(t)
        self.assertEqual(tokens[0].type, "DOC_STRING")
        self.assertEqual(
            [
                tokens[10].type,
                tokens[10].value,
                tokens[10].lineno,
                tokens[10].index,
                tokens[10].end,
            ],
            ["KW_FROM", "from", 9, 166, 170],
        )
        self.assertEqual(
            [
                tokens[-1].type,
                tokens[-1].value,
                tokens[-1].lineno,
                tokens[-1].index,
                tokens[-1].end,
            ],
            ["RBRACE", "}", 61, 1422, 1423],
        )
