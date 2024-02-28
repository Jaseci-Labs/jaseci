"""Test pass module."""

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import DeclDefMatchPass
from jaclang.utils.test import TestCase


class DeclDefMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base.jac"), DeclDefMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(c)say_hi"].decl.body)
        self.assertIn("(o)Test.(c)__init__", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(c)__init__"].decl.body)

    def test_ability_connected_to_decl_post(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base2.jac"), DeclDefMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(c)say_hi"].decl.body)
        self.assertIn("(o)Test.(c)__init__", state.ir.sym_tab.tab)
        self.assertIsNotNone(state.ir.sym_tab.tab["(o)Test.(c)__init__"].decl.body)
