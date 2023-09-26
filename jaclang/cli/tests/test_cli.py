"""Test Jac cli module."""
import io
import sys

from jaclang.cli import cmds
from jaclang.utils.test import TestCase


class JacCliTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli_run(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cmds.run(self.fixture_abs_path("hello.jac"))  # type: ignore

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertIn("Hello World!", stdout_value)

    def test_jac_cli_err_output(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        # Execute the function
        try:
            cmds.enter(self.fixture_abs_path("err.jac"), entrypoint="speak", args=[])  # type: ignore
        except Exception as e:
            print(f"Error: {e}")

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdout_value = captured_output.getvalue()
        # print(stdout_value)
        # Assertions or verifications
        self.assertIn("*4:", stdout_value)
        self.assertIn("*7:", stdout_value)

    def test_jac_cli_alert_based_err(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        # Execute the function
        try:
            cmds.enter(self.fixture_abs_path("err2.jac"), entrypoint="speak", args=[])  # type: ignore
        except Exception as e:
            print(f"Error: {e}")

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdout_value = captured_output.getvalue()
        # print(stdout_value)
        # Assertions or verifications
        self.assertIn("Errors occured", stdout_value)

    def test_jac_ast_tool_pass_template(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cmds.ast_tool("pass_template")  # type: ignore

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        # print(stdout_value)
        # Assertions or verifications
        self.assertIn("Sub objects.", stdout_value)
        self.assertGreater(stdout_value.count("def exit_"), 10)

    def test_jac_ast_tool_keywords(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cmds.ast_tool("jac_keywords")  # type: ignore

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        # print(stdout_value)
        # Assertions or verifications
        self.assertIn("walker", stdout_value)
        self.assertGreater(stdout_value.count("|"), 10)
