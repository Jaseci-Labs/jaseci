"""Test pass module."""
from jaclang.jac.passes.decl_def_match_pass import DeclDefMatchPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class DeclDefMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_import_values_avail(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            "base.jac", self.fixture_abs_path(""), DeclDefMatchPass
        )
        self.assertFalse(state.errors_had)
        self.assertIn("mine", state.sym_tab.tab)
        self.assertIsNotNone(state.sym_tab.tab["mine"].node.body)

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            "base.jac", self.fixture_abs_path(""), DeclDefMatchPass
        )
        self.assertFalse(state.errors_had)
        self.assertIn("Test.say_hi", state.sym_tab.tab)
        self.assertIsNotNone(state.sym_tab.tab["Test.say_hi"].node.body)
