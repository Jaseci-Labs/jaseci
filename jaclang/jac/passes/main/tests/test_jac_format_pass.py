"""Test ast build pass module."""

from jaclang.jac.passes.main import JacFormatPass
from jaclang.jac.passes.main import PyastGenPass
from jaclang.jac.passes.main.schedules import py_code_gen as without_format
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class JacFormatPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = JacFormatPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("base.jac"), target=JacFormatPass
        )
        self.assertFalse(code_gen.errors_had)

    def test_empty_codeblock(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("base.jac"), target=JacFormatPass
        )
        self.assertFalse(code_gen.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename),
            target=PyastGenPass,
            schedule=without_format,
        )
        with_format = [JacFormatPass]
        with_format.extend(without_format)
        code_gen2 = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyastGenPass, schedule=with_format
        )
        for i in range(len(code_gen.ir.gen.py.split("\n"))):
            if "test_" in code_gen.ir.gen.py.split("\n")[i]:
                continue
            self.assertEqual(
                code_gen.ir.gen.py.split("\n")[i], code_gen2.ir.gen.py.split("\n")[i]
            )


JacFormatPassTests.self_attach_micro_tests()
