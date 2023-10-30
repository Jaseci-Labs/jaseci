"""Test ast build pass module."""
from jaclang.jac.passes.blue import JacFormatPass
from jaclang.jac.transpiler import jac_file_formatter
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class JacFormatPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = JacFormatPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_formatter(self.fixture_abs_path("base.jac"))
        self.assertFalse(code_gen.errors_had)

    def test_empty_codeblock(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_formatter(self.fixture_abs_path("base.jac"))
        self.assertFalse(code_gen.errors_had)
        # self.assertIn("pass", code_gen.ir.gen.jac)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_formatter(self.fixture_abs_path(filename))
        self.assertGreater(len(code_gen.ir.gen.jac), 10)


JacFormatPassTests.self_attach_micro_tests()
