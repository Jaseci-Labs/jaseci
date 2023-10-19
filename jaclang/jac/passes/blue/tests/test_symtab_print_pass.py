"""Test pass module."""
import os

from jaclang.jac.passes.blue.schedules import SymbolTablePrinterPass, sym_tab_print
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class SymbolTablePrinterPassTest(TestCase):
    """Test pass module."""

    TargetPass = SymbolTablePrinterPass

    def setUp(self) -> None:
        """Set up test."""
        if os.path.isfile("out.txt"):
            os.remove("out.txt")
        return super().setUp()

    def test_report_generation(self) -> None:
        """Basic test for pass."""
        SymbolTablePrinterPass.SAVE_OUTPUT = "out.txt"
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"), "", SymbolTablePrinterPass, sym_tab_print
        )
        self.assertFalse(state.errors_had)

        with open("out.txt") as f:
            res_lines = "".join(f.readlines())

        with open(self.fixture_abs_path("multi_def_err.symtab_txt")) as f:
            ref_lines = "".join(f.readlines())

        self.assertEqual(res_lines, ref_lines)
