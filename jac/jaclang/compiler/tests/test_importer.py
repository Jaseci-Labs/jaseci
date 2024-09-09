"""Tests for Jac Loader."""

import io
import sys

from jaclang import jac_import
from jaclang.cli import cli
from jaclang.runtimelib.machine import JacMachine, JacProgram
from jaclang.utils.test import TestCase


class TestLoader(TestCase):
    """Test Jac self.prse."""

    def test_import_basic_python(self) -> None:
        """Test basic self loading."""
        JacMachine(self.fixture_abs_path(__file__)).attach_program(
            JacProgram(mod_bundle=None, bytecode=None)
        )
        (h,) = jac_import("fixtures.hello_world", base_path=__file__)
        self.assertEqual(h.hello(), "Hello World!")  # type: ignore
        JacMachine.detach()

    def test_modules_correct(self) -> None:
        """Test basic self loading."""
        JacMachine(self.fixture_abs_path(__file__)).attach_program(
            JacProgram(mod_bundle=None, bytecode=None)
        )
        jac_import("fixtures.hello_world", base_path=__file__)
        self.assertIn(
            "module 'fixtures.hello_world'",
            str(JacMachine.get().loaded_modules),
        )
        self.assertIn(
            "/tests/fixtures/hello_world.jac",
            str(JacMachine.get().loaded_modules),
        )
        JacMachine.detach()

    def test_jac_py_import(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.run(self.fixture_abs_path("../../../tests/fixtures/jp_importer.jac"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Hello World!", stdout_value)
        self.assertIn(
            "{SomeObj(a=10): 'check'} [MyObj(apple=5, banana=7), MyObj(apple=5, banana=7)]",
            stdout_value,
        )

    def test_jac_py_import_auto(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.run(self.fixture_abs_path("../../../tests/fixtures/jp_importer_auto.jac"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Hello World!", stdout_value)
        self.assertIn(
            "{SomeObj(a=10): 'check'} [MyObj(apple=5, banana=7), MyObj(apple=5, banana=7)]",
            stdout_value,
        )
