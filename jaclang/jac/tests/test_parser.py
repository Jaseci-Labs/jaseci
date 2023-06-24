"""Tests for Jac parser."""
from jaclang.jac.absyntree import AstNode
from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCaseMicroSuite


class TestParser(TestCaseMicroSuite):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        lex = JacLexer(mod_path="", input_ir=self.file_to_str(filename)).ir
        prse = JacParser(mod_path="", input_ir=lex)
        self.assertFalse(prse.had_error)

    def test_shift_reduce_conflict(self) -> None:
        """Test for shift reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.sr_conflicts), 0)

    def test_reduce_reduce_conflict(self) -> None:
        """Test for reduce reduce conflict."""
        self.assertEqual(len(JacParser._lrtable.rr_conflicts), 0)

    def test_basci_parsing(self) -> None:
        """Basic test for parsing."""
        lex = JacLexer(mod_path="", input_ir=self.load_fixture("fam.jac")).ir
        prse = JacParser(mod_path="", input_ir=lex)
        output = prse.ir
        self.assertFalse(prse.had_error)
        if isinstance(output, AstNode):
            self.assertGreater(len(str(output.to_dict())), 1000)
        else:
            self.fail("Output is not an AstNode.")

    def test_parsing_jac_cli(self) -> None:
        """Basic test for parsing."""
        lex = JacLexer(
            mod_path="", input_ir=self.load_fixture("../../../cli/jac_cli.jac")
        ).ir
        prse = JacParser(mod_path="", input_ir=lex)
        self.assertFalse(prse.had_error)


TestParser.self_attach_micro_tests()