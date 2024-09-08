"""Test pass module."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import DeclImplMatchPass
from jaclang.utils.test import TestCase


class DeclImplMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base.jac"), DeclImplMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)say_hi"].decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)__init__"].decl.name_of.body
        )

    def test_ability_connected_to_decl_post(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base2.jac"), DeclImplMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)say_hi"].decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)__init__"].decl.name_of.body
        )

    def test_arch_ref_has_sym(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("defs_and_uses.jac"), DeclImplMatchPass
        )
        for i in state.ir.get_all_sub_nodes(ast.ArchRef):
            self.assertIsNotNone(i.sym)
