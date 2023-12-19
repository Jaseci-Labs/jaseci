"""Test pass module."""
import os

from jaclang.compiler.passes.tool.schedules import (
    SymbolTableDotGraphPass,
    SymbolTablePrinterPass,
    sym_tab_print,
)
from jaclang.compiler.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class SymbolTablePrinterPassTest(TestCase):
    """Test pass module."""

    TargetPass = SymbolTablePrinterPass

    def setUp(self) -> None:
        """Set up test."""
        if os.path.isfile("out.txt"):
            os.remove("out.txt")
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down test."""
        if os.path.isfile("out.txt"):
            os.remove("out.txt")
        return super().tearDown()

    def test_report_generation(self) -> None:
        """Basic test for pass."""
        SymbolTablePrinterPass.SAVE_OUTPUT = "out.txt"
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"),
            SymbolTablePrinterPass,
            sym_tab_print,
        )
        self.assertFalse(state.errors_had)

        with open("out.txt") as f:
            res_lines = "".join(f.readlines())

        for i in ["MyObject", "AnotherObject", "line 5, col 1", "line 3, col 1"]:
            self.assertIn(i, res_lines)


class DotGraphDrawerPassTests(TestCase):
    """Test pass module."""

    TargetPass = SymbolTableDotGraphPass

    def setUp(self) -> None:
        """Set up test."""
        if os.path.isfile("out.dot"):
            os.remove("out.dot")
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down test."""
        if os.path.isfile("out.dot"):
            os.remove("out.dot")
        return super().tearDown()

    def test_report_generation(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"), SymbolTableDotGraphPass
        )
        self.assertFalse(state.errors_had)

        with open("out.dot") as f:
            res_lines = "".join(f.readlines())

        for i in ["MyObject", "AnotherObject", "line 5, col 1", "line 3, col 1"]:
            self.assertIn(i, res_lines)
