"""Test pass module."""
from jaclang.jac.passes.blue import DeclDefMatchPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class DeclDefMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("base.jac"), "", DeclDefMatchPass
        )
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(a)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(a)say_hi"].decl.body)
        self.assertIn("(o)Test.(a)init", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(a)init"].decl.body)

    def test_ability_connected_to_decl_post(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("base2.jac"), "", DeclDefMatchPass
        )
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(a)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(a)say_hi"].decl.body)
        self.assertIn("(o)Test.(a)init", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(a)init"].decl.body)

    def test_collision_error_correct(self) -> None:
        """Basic test for multi defs."""
        state = jac_file_to_pass(
            self.fixture_abs_path("decls.jac"), "", DeclDefMatchPass
        )
        self.assertTrue(state.warnings_had)
        self.assertIn("/impl/defs2.jac", str(state.warnings_had[0]))
        self.assertIn("/impl/defs1.jac", str(state.warnings_had[0]))
        self.assertIn("/impl/defs2.jac", str(state.warnings_had[1]))
        self.assertIn("/impl/defs1.jac", str(state.warnings_had[1]))
