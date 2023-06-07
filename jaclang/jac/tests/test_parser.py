"""Tests for Jac parser."""

from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCase


class TestParser(TestCase):
    """Test Jac parser."""

    def test_basci_parsing(self: "TestParser") -> None:
        """Basic test for lexer."""
        lexer = JacLexer()
        parser = JacParser()
        output = parser.parse(lexer.tokenize(self.load_fixture("fam.jac")))
        self.assertFalse(parser.had_error)
        self.assertGreater(len(str(output)), 1000)

    def test_shift_reduce_conflict(self: "TestParser") -> None:
        """Test for shift reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.sr_conflicts), 0)

    def test_reduce_reduce_conflict(self: "TestParser") -> None:
        """Test for reduce reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.rr_conflicts), 0)
