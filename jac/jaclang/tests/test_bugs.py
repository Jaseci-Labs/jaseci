"""Test Jac language generally."""

from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class JacBugTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_impl_match_confusion_issue(self) -> None:
        """Basic test for symtable support for inheritance."""
        (mypass := JacProgram()).compile(
            self.fixture_abs_path("impl_match_confused.jac"),
        )
        self.assertEqual(len(mypass.errors_had), 1)
