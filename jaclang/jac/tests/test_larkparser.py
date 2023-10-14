"""Tests for Jac parser."""
from jaclang.jac import jac_lark as jl
from jaclang.jac.absyntree import SourceString
from jaclang.jac.constant import Tokens
from jaclang.jac.larkparse import JacParser
from jaclang.utils.test import TestCaseMicroSuite


class TestLarkParser(TestCaseMicroSuite):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_fstring_escape_brace(self) -> None:
        """Test fstring escape brace."""
        source = SourceString('global a=f"{{}}", not_b=4;')
        prse = JacParser(mod_path="", input_ir=source, prior=None)
        self.assertFalse(prse.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            mod_path=filename,
            input_ir=SourceString(self.file_to_str(filename)),
            prior=None,
        )
        self.assertFalse(prse.errors_had)

    def test_parser_fam(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            mod_path="",
            input_ir=SourceString(self.load_fixture("fam.jac")),
            prior=None,
        )
        self.assertFalse(prse.errors_had)

    def test_parser_kwesc(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            mod_path="",
            input_ir=SourceString(self.load_fixture("kwesc.jac")),
            prior=None,
        )
        self.assertFalse(prse.errors_had)

    def test_parser_mod_doc_test(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            mod_path="",
            input_ir=SourceString(self.load_fixture("mod_doc_test.jac")),
            prior=None,
        )
        self.assertFalse(prse.errors_had)

    def test_enum_matches_lark_toks(self) -> None:
        """Test that enum stays synced with lexer."""
        tokens = [x.name for x in jl.Lark_StandAlone().parser.lexer_conf.terminals]
        for token in tokens:
            self.assertIn(token, Tokens.__members__)
        for token in Tokens:
            self.assertIn(token.name, tokens)
        for token in Tokens:
            self.assertIn(token.value, tokens)


TestLarkParser.self_attach_micro_tests()
