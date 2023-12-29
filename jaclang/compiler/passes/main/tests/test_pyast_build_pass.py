"""Test pass module."""
import ast as py_ast
import inspect

from jaclang.compiler.passes.main import PyastBuildPass
from jaclang.utils.helpers import pascal_to_snake
from jaclang.utils.test import TestCase


class PyastBuildPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_synced_to_latest_py_ast(self) -> None:
        """Basic test for pass."""
        visit_methods = [
            method for method in dir(py_ast._Unparser) if method.startswith("visit_")  # type: ignore
        ]
        node_names = [
            pascal_to_snake(method.replace("visit_", "")) for method in visit_methods
        ]
        pass_func_names = []
        for name, value in inspect.getmembers(PyastBuildPass):
            if name.startswith("proc_") and inspect.isfunction(value):
                pass_func_names.append(name.replace("proc_", ""))
        for name in pass_func_names:
            self.assertIn(name, node_names)  # type: ignore
        for name in node_names:
            self.assertIn(name, pass_func_names)  # type: ignore
