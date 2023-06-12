"""Tests for Jac self.prse."""
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

    def test_micro_decl_defs_imp(self: "TestParser") -> None:
        """Test for declaration, definition, and import."""
        self.parse_micro("decl_defs_imp.jac")

    def test_micro_decl_defs_split(self: "TestParser") -> None:
        """Test for declaration, definition, and import."""
        self.parse_micro("decl_defs_split.jac")

    def test_micro_module_structure(self: "TestParser") -> None:
        """Test for module structure."""
        self.parse_micro("module_structure.jac")

    def test_micro_whitespace(self: "TestParser") -> None:
        """Test for whitespace."""
        self.parse_micro("whitespace.jac")

    def test_micro_type_hints(self: "TestParser") -> None:
        """Test for type hints."""
        self.parse_micro("type_hints.jac")

    def test_micro_no_here(self: "TestParser") -> None:
        """Test for no here."""
        self.parse_micro("no_here.jac")

    def test_micro_access_info(self: "TestParser") -> None:
        """Test for access info."""
        self.parse_micro("access_info.jac")

    def test_micro_separate_defs(self: "TestParser") -> None:
        """Test for separate defs."""
        self.parse_micro("separate_defs.jac")

    def test_micro_jac_files_fully_tested(self: "TestParser") -> None:
        """Test that all micro jac files are fully tested."""
        self.directory = os.path.dirname(__file__) + "/fixtures/micro"
        for filename in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, filename)):
                method_name = f"test_micro_{filename.replace('.jac', '')}"
                self.assertIn(method_name, dir(self))
