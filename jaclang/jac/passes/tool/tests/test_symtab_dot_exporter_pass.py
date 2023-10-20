"""Test pass module."""
import os

from jaclang.jac.passes.tool import SymtabDotGraphPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class DotGraphDrawerPassTests(TestCase):
    """Test pass module."""

    TargetPass = SymtabDotGraphPass

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
            self.fixture_abs_path("multi_def_err.jac"), "", SymtabDotGraphPass
        )
        self.assertFalse(state.errors_had)

        with open("out.dot") as f:
            res_lines = "".join(f.readlines())

        with open(self.fixture_abs_path("symtab_multi_def_err.dot")) as f:
            ref_lines = "".join(f.readlines())

        self.assertEqual(res_lines, ref_lines)
