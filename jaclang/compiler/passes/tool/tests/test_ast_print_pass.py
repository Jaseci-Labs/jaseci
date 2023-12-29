"""Test pass module."""
import os

from jaclang.compiler.passes.tool import AstDotGraphPass, AstPrinterPass
from jaclang.compiler.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class DotGraphDrawerPassTests(TestCase):
    """Test pass module."""

    TargetPass = AstDotGraphPass

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
            self.fixture_abs_path("multi_def_err.jac"), AstDotGraphPass
        )
        self.assertFalse(state.errors_had)

        with open("out.dot") as f:
            res_lines = "".join(f.readlines())

        # print(res_lines)
        with open(self.fixture_abs_path("multi_def_err.dot")) as f:
            ref_lines = "".join(f.readlines())

        self.assertEqual(res_lines.strip(), ref_lines.strip())


class AstPrinterPassTest(TestCase):
    """Test pass module."""

    TargetPass = AstPrinterPass

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
        AstPrinterPass.SAVE_OUTPUT = "out.txt"
        state = jac_file_to_pass(
            self.fixture_abs_path("multi_def_err.jac"), AstPrinterPass
        )
        self.assertFalse(state.errors_had)

        with open("out.txt") as f:
            res_lines = "".join(f.readlines())

        # print(res_lines)
        with open(self.fixture_abs_path("multi_def_err.txt")) as f:
            ref_lines = "".join(f.readlines())
        self.assertEqual(res_lines.split(), ref_lines.split())
