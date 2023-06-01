"""Test transpiler."""
from jaseci.jac.transpile import JacTranspiler
from jaseci.utils.test import TestCase


class TestTranspiler(TestCase):
    """Test Jac transpiler."""

    def test_core_transpiler_loop(self: "TestTranspiler") -> None:
        """Basic test for transpiler."""
        transpiler = JacTranspiler()
        output = transpiler.transpile(self.load_fixture("fam.jac"))
        self.assertIsNotNone(output)
