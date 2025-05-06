"""Test for Access Modifier pass."""

import io
import sys

from jaclang.cli import cli
from jaclang.compiler.passes.main import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class TestAccessModifierPass(TestCase):
    """Test the access modifier pass for the Jac compiler."""

    def test_access_modifier(self) -> None:
        """Test for access tags working."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output
        cli.check(
            self.fixture_abs_path("access_modifier.jac"),
            print_errs=True,
        )
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.count("Invalid access"), 18)

    def test_access_modifier_pass_directly(self) -> None:
        """Test the access modifier pass directly by compiling a program."""
        (prog := JacProgram()).compile(
            self.fixture_abs_path("access_modifier.jac"),
            mode=CMode.TYPECHECK,
        )

        # Count errors related to invalid access
        access_errors = [
            err for err in prog.errors_had if "Invalid access" in str(err.msg)
        ]
        self.assertEqual(len(access_errors), 18)

        # Verify some specific error messages
        error_messages = [str(err.msg) for err in access_errors]
        self.assertTrue(
            any(
                'Invalid access of private member "InnerPrivObj"' in msg
                for msg in error_messages
            )
        )
        self.assertTrue(
            any(
                'Invalid access of protected member "InnerProtObj"' in msg
                for msg in error_messages
            )
        )
        self.assertTrue(
            any(
                'Invalid access of private member "priv_attrib"' in msg
                for msg in error_messages
            )
        )
