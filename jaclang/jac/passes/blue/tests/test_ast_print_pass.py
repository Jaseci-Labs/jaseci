"""Test pass module."""
import os

from jaclang.jac.passes.blue import ASTPrinterPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class AstPrinterPassTest(TestCase):
    """Test pass module."""

    TargetPass = ASTPrinterPass

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
        ASTPrinterPass.SAVE_OUTPUT = "out.txt"
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"), "", ASTPrinterPass
        )
        self.assertFalse(state.errors_had)

        with open("out.txt") as f:
            res_lines = "".join(f.readlines())

        with open(self.fixture_abs_path("multi_def_err.txt")) as f:
            ref_lines = "".join(f.readlines())

        self.assertEqual(res_lines, ref_lines)
