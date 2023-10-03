"""Tests for Jac parser."""
from jaclang.jac.larkparse import JacParser
from jaclang.utils.test import TestCaseMicroSuite


class TestLarkParser(TestCaseMicroSuite):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        prse = JacParser(mod_path=filename, input_ir=self.file_to_str(filename))
        print(prse.ir.pretty())
        self.assertFalse(prse.errors_had)


TestLarkParser.self_attach_micro_tests()
