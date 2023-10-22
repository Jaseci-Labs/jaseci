"""Test pass module."""
from jaclang.jac.passes.blue import DefUsePass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class DefUsePassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_def_uses(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            file_path=self.fixture_abs_path("defs_and_uses.jac"),
            base_dir="",
            target=DefUsePass,
        )
        self.assertEqual(len(state.warnings_had), 0)
        self.assertEqual(len(state.errors_had), 0)
