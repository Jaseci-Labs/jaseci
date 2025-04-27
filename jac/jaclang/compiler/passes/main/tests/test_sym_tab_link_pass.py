"""Test SymTable Link Pass."""

import os

from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class SymTabLinkPassTests(TestCase):
    """Test pass module."""

    # Need change
    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_registry_pass(self) -> None:
        """Basic test for pass."""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "symtab_link_tests",
            "no_dupls.jac",
        )
        mod = JacProgram().compile(file_path, schedule=py_code_gen_typed)
        self.assertEqual(
            len(mod.sym_tab.names_in_scope.values()),
            3,
        )
        for i in ["[Symbol(a,", "Symbol(Man,", "Symbol(p,"]:
            self.assertIn(
                i,
                str(mod.sym_tab.names_in_scope.values()),
            )
        self.assertEqual(len(mod.sym_tab.names_in_scope["a"].uses), 2)
        self.assertEqual(
            len(
                list(
                    mod.sym_tab.kid_scope[0]
                    .kid_scope[0]
                    .kid_scope[0]
                    .kid_scope[0]
                    .inherited_scope[0]
                    .base_symbol_table.names_in_scope.values()
                )[0].uses,
            ),
            3,
        )
