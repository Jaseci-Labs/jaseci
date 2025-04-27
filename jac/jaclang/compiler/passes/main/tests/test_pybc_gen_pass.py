"""Test pass module."""

import marshal

from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class PyBytecodeGenPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_simple_bcgen(self) -> None:
        """Basic test for pass."""
        jac_code = JacProgram().compile(
            file_path=self.fixture_abs_path("func.jac"),
        )
        try:
            marshal.loads(jac_code.gen.py_bytecode)
            self.assertTrue(True)
        except ValueError:
            self.fail("Invalid bytecode generated")
