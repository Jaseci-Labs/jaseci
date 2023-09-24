"""Tests for the PurplePygenPass."""
import io
import sys

from jaclang import core
from jaclang import jac_purple_import
from jaclang.jac.passes.purple import PurplePygenPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCaseMicroSuite


class PurplePygenPassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        core.exec_ctx.reset()
        return super().setUp()

    def test_simple_jac_red(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_purple_import(
            "micro.simple_walk", self.fixture_abs_path("../../../../../../examples/")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "Value: -1\nValue: 0\nValue: 1\nValue: 2\nValue: 3\nValue: 4"
            "\nValue: 5\nValue: 6\nValue: 7\nFinal Value: 8\nDone walking.\n",
        )

    def test_guess_game(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_purple_import("guess_game", self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "Too high!\nToo low!\nToo high!\nCongratulations! You guessed correctly.\n",
        )

    def test_ignore(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_purple_import("ignore", self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.split("\n")[0].count("here"), 10)
        self.assertEqual(stdout_value.split("\n")[1].count("here"), 5)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PurplePygenPass
        )
        self.assertGreater(len(code_gen.ir.meta["py_code"]), 10)


PurplePygenPassTests.self_attach_micro_tests()
