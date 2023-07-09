"""Tests for the PurplePygenPass."""
from jaclang.jac.transpiler import transpile_jac_purple
from jaclang.utils.test import TestCaseMicroSuite


class PurplePygenPassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = transpile_jac_purple(filename, "")
        self.assertGreater(len(code_gen), 10)


PurplePygenPassTests.self_attach_micro_tests()
