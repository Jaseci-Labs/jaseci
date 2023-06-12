"""Tests for Jac parser."""
import os

from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCase


class TestParser(TestCase):
    """Test Jac self.prse."""

    def setUp(self: TestCase) -> None:
        """Set up test."""
        self.lex = JacLexer()
        self.prse = JacParser()
        return super().setUp()

    def parse_micro(self: "TestParser", filename: str) -> None:
        """Parse micro jac file."""
        self.prse.cur_file = filename
        self.prse.parse(self.lex.tokenize(self.load_fixture(f"micro/{filename}")))
        self.assertFalse(self.prse.had_error)

    @classmethod
    def self_attach_micro_tests(cls: "TestParser") -> None:
        """Attach micro tests."""
        directory = os.path.dirname(__file__) + "/fixtures/micro"
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(
                ".jac"
            ):
                method_name = f"test_micro_{filename.replace('.jac', '')}"
                setattr(cls, method_name, lambda self, f=filename: self.parse_micro(f))

    def test_shift_reduce_conflict(self: "TestParser") -> None:
        """Test for shift reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.sr_conflicts), 0)

    def test_reduce_reduce_conflict(self: "TestParser") -> None:
        """Test for reduce reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.rr_conflicts), 0)

    def test_basci_parsing(self: "TestParser") -> None:
        """Basic test for parsing."""
        output = self.prse.parse(self.lex.tokenize(self.load_fixture("fam.jac")))
        self.assertFalse(self.prse.had_error)
        self.assertGreater(len(str(output)), 1000)

    def test_micro_jac_files_fully_tested(self: "TestParser") -> None:
        """Test that all micro jac files are fully tested."""
        self.directory = os.path.dirname(__file__) + "/fixtures/micro"
        for filename in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, filename)):
                method_name = f"test_micro_{filename.replace('.jac', '')}"
                self.assertIn(method_name, dir(self))


TestParser.self_attach_micro_tests()
