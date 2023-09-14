"""Test pass module."""
from jaclang.jac.passes.blue import SymTabBuildPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class SymTabBuildPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_name_collision(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"), "", SymTabBuildPass
        )
        self.assertGreater(len(state.errors_had), 0)
        self.assertIn("MyObject", str(state.errors_had[0]))
