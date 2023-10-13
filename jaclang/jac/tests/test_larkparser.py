"""Tests for Jac parser."""
from jaclang.jac.absyntree import SourceString
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
        # out = prse.ir.pretty()
        self.assertFalse(prse.errors_had)
        # self.assertIn("not_b", out)
        # self.assertIn("{{", out)
        # self.assertIn("}}", out)
        # self.assertIn("fstring", out)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            mod_path=filename,
            input_ir=SourceString(self.file_to_str(filename)),
            prior=None,
        )
        self.assertFalse(prse.errors_had)


TestLarkParser.self_attach_micro_tests()
