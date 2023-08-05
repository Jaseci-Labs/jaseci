"""Tests for Jac lexer."""
from typing import Generator

from jaclang.jac.constant import Tokens
from jaclang.jac.lexer import JacLexer
from jaclang.utils.test import TestCase


class TestLexer(TestCase):
    """Test Jac lexer."""

    def test_lexer(self) -> None:
        """Basic test for lexer."""
        tokens = []
        ir = JacLexer(mod_path="", input_ir=self.load_fixture("lexer_fam.jac")).ir
        if not isinstance(ir, Generator):
            raise ValueError("Lexer did not return generator.")
        for t in ir:
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
            ["KW_FROM", "from", 9, 140, 144],
        )
        self.assertEqual(
            [
                tokens[-1].type,
                tokens[-1].value,
                tokens[-1].lineno,
            ],
            ["RBRACE", "}", 61],
        )

    def test_col_idxs(self) -> None:
        """Basic test for lexer."""
        tokens = []
        ir = JacLexer(mod_path="", input_ir=self.load_fixture("lexer_fam.jac")).ir
        if not isinstance(ir, Generator):
            raise ValueError("Lexer did not return generator.")
        for t in ir:
            tokens.append((t.value, t.lineno, t.index - t.lineidx, t.end - t.lineidx))
        self.assertEqual(tokens[12], ("activity", 9, 16, 24))
        self.assertEqual(tokens[-3], ("outside_func", 59, 24, 36))

    def test_enum_matches_lexer_toks(self) -> None:
        """Test that enum stays synced with lexer."""
        for token in JacLexer.tokens:
            self.assertIn(token, Tokens.__members__)
        for token in Tokens:
            self.assertIn(token.name, JacLexer.tokens)
        for token in Tokens:
            self.assertIn(token.value, JacLexer.tokens)
