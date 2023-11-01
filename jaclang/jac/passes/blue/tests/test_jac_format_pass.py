"""Test ast build pass module."""
import io
import sys

from jaclang.cli import cmds
from jaclang.jac.passes.blue import JacFormatPass
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
        # self.assertIn("pass", code_gen.ir.gen.jac)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=JacFormatPass
        )
        self.assertGreater(len(code_gen.ir.gen.jac), 10)

    # def test_circle_jac(self) -> None:
    #     """Basic test for pass."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output

    #     # Execute the function
    #     cmds.run(
    #         self.fixture_abs_path("../../../../../examples/manual_code/circle.jac")
    #     )  # type: ignore

    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()

    #     # Assertions or verifications
    #     self.assertIn(
    #         "Area of a circle with radius 5 using function: 78",
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         "Area of a Circle with radius 5 using class: 78",
    #         stdout_value,
    #     )

    # def test_circle_jac_test(self) -> None:
    #     """Basic test for pass."""
    #     captured_output = io.StringIO()
    #     sys.stderr = captured_output

    #     # Execute the function
    #     cmds.test(
    #         self.fixture_abs_path("../../../../examples/manual_code/circle.jac")
    #     )  # type: ignore

    #     sys.stderr = sys.__stderr__
    #     stderr_value = captured_output.getvalue()
    #     # Assertions or verifications
    #     self.assertIn("Ran 3 tests", stderr_value)

    # def test_clean_circle_jac(self) -> None:
    #     """Basic test for pass."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output

    #     # Execute the function
    #     cmds.run(
    #         self.fixture_abs_path("../../../../examples/manual_code/circle.jac")
    #     )  # type: ignore
    #     stdout_value = captured_output.getvalue()
    #     sys.stdout = sys.__stdout__
    #     print(stdout_value)
    #     # Assertions or verifications
    #     self.assertIn(
    #         "Area of a circle with radius 5 using function: 78",
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         "Area of a Circle with radius 5 using class: 78",
    #         stdout_value,
    #     )

    # def test_clean_circle_jac_test(self) -> None:
    #     """Basic test for pass."""
    #     captured_output = io.StringIO()
    #     sys.stderr = captured_output

    #     # Execute the function
    #     cmds.test(
    #         self.fixture_abs_path(
    #             "../../../../examples/manual_code/circle_clean_tests.jac"
    #         )
    #     )  # type: ignore

    #     sys.stderr = sys.__stderr__
    #     stderr_value = captured_output.getvalue()
    #     # Assertions or verifications
    #     self.assertIn("Ran 3 tests", stderr_value)


JacFormatPassTests.self_attach_micro_tests()
