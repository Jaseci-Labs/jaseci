"""Test Jac cli module."""

import io
import sys
from contextlib import suppress

from jaclang.cli import cli
from jaclang.utils.test import TestCase
from jaclang.settings import settings


class JacCliTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_circle_jac(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.examples_abs_path("manual_code/circle.jac"))

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertIn(
            "Area of a circle with radius 5 using function: 78",
            stdout_value,
        )
        self.assertIn(
            "Area of a Circle with radius 5 using class: 78",
            stdout_value,
        )

    def test_circle_jac_test(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        stdout_block = io.StringIO()
        sys.stderr = captured_output
        sys.stdout = stdout_block

        # Execute the function
        cli.test(self.examples_abs_path("manual_code/circle.jac"))

        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        stderr_value = captured_output.getvalue()
        # Assertions or verifications
        self.assertIn("Ran 3 tests", stderr_value)

    def test_clean_circle_jac(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.examples_abs_path("manual_code/circle_clean.jac"))

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertEqual(
            "Area of a circle with radius 5 using function: 78.53981633974483\n"
            "Area of a Circle with radius 5 using class: 78.53981633974483\n",
            stdout_value,
        )

    def test_pure_circle_jac(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.examples_abs_path("manual_code/circle_pure.jac"))

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertEqual(
            "Area of a circle with radius 5 using function: 78.53981633974483\n"
            "Area of a Circle with radius 5 using class: 78.53981633974483\n",
            stdout_value,
        )

    def test_pure_circle_impl_not_double_generated(self) -> None:
        """Basic test for pass."""
        old_setting = settings.enable_jac_semantics
        settings.enable_jac_semantics = False
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cli.tool(
            "ir",
            [
                "py",
                f"{self.examples_abs_path('manual_code/circle_pure.jac')}",
            ],
        )

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        settings.enable_jac_semantics = old_setting

        # Assertions or verifications
        self.assertNotIn("\ndef __init__(self", stdout_value)

    def test_clean_circle_jac_test(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        stdio_block = io.StringIO()
        sys.stderr = captured_output
        sys.stdout = stdio_block

        # Execute the function
        with suppress(SystemExit):
            cli.test(self.examples_abs_path("manual_code/circle_clean_tests.jac"))

        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        stderr_value = captured_output.getvalue()
        # Assertions or verifications
        self.assertIn("Ran 3 tests", stderr_value)

    def test_pure_circle_jac_test(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        stdio_block = io.StringIO()
        sys.stderr = captured_output
        sys.stdout = stdio_block

        # Execute the function
        with suppress(SystemExit):
            cli.test(self.examples_abs_path("manual_code/circle_pure.test.jac"))

        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        stderr_value = captured_output.getvalue()
        # Assertions or verifications
        self.assertIn("Ran 3 tests", stderr_value)

    def test_jac_name_in_sys_mods(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.fixture_abs_path("../../../jaclang/tests/fixtures/abc_check.jac"))

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertIn(
            "Area of a circle with radius 5 using function: 78",
            stdout_value,
        )
        self.assertIn(
            "Area of a Circle with radius 5 using class: 78",
            stdout_value,
        )
