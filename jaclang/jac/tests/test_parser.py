"""Tests for Jac self.p."""

from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCase

import os


class TestParser(TestCase):
    """Test Jac self.p."""

    def setUp(self: TestCase) -> None:
        self.l = JacLexer()
        self.p = JacParser()
        return super().setUp()
    
    def parse_micro(self: "TestParser", filename: str) -> None:
        """Parse micro jac file."""
        self.p.parse(self.l.tokenize(self.load_fixture(f'micro/{filename}')))
        self.assertFalse(self.p.had_error)

    def test_shift_reduce_conflict(self: "TestParser") -> None:
        """Test for shift reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.sr_conflicts), 0)

    def test_reduce_reduce_conflict(self: "TestParser") -> None:
        """Test for reduce reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.rr_conflicts), 0)

    def test_basci_parsing(self: "TestParser") -> None:
        """Basic test for parsing."""

        output = self.p.parse(self.l.tokenize(self.load_fixture("fam.jac")))
        self.assertFalse(self.p.had_error)
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


    def test_micro_jac_files_fully_tested(self: "TestParser") -> None:
        """Test that all micro jac files are fully tested."""
        self.directory = os.path.dirname(__file__) + "/fixtures/micro"
        for filename in os.listdir(self.directory):
            print(filename)
            if os.path.isfile(os.path.join(self.directory, filename)):
                method_name = f"test_micro_{filename.replace('.jac', '')}"
                self.assertIn(method_name, dir(self))