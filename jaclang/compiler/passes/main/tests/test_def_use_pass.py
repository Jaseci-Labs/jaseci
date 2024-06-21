"""Test pass module."""

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import DefUsePass
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
            target=DefUsePass,
        )
        uses = [i.uses for i in state.ir.sym_tab.kid[0].tab.values()]
        self.assertEqual(len(uses[1]), 1)
        self.assertEqual(len(uses[2]), 1)
        self.assertIn("output", [uses[1][0].sym_name, uses[2][0].sym_name])
        self.assertIn("message", [uses[1][0].sym_name, uses[2][0].sym_name])
