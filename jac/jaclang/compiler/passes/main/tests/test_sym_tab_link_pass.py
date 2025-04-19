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
        mod = JacProgram.jac_file_to_pass(file_path, schedule=py_code_gen_typed).root_ir
        self.assertEqual(
            len(mod.sym_tab.tab.values()),
            3,
        )
        for i in ["[Symbol(a,", "Symbol(Man,", "Symbol(p,"]:
            self.assertIn(
                i,
                str(mod.sym_tab.tab.values()),
            )
        self.assertEqual(len(mod.sym_tab.tab["a"].uses), 2)
        self.assertEqual(
            len(
                list(
                    mod.sym_tab.kid[0]
                    .kid[0]
                    .kid[0]
                    .kid[0]
                    .inherit[0]
                    .base_symbol_table.tab.values()
                )[0].uses,
            ),
            3,
        )
