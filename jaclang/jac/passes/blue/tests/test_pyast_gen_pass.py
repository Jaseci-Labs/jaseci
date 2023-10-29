"""Test ast build pass module."""
from jaclang.jac.passes.blue import PyAstGenPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class PyAstGenPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = PyAstGenPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../cli/cli.jac"), target=PyAstGenPass
        )
        self.assertFalse(code_gen.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyAstGenPass
        )
        self.assertGreater(len(code_gen.ir.meta["py_code"]), 10)


PyAstGenPassTests.self_attach_micro_tests()
