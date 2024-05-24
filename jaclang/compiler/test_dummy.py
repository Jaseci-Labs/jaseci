"""Test Jac language generally."""

import io
import os
import sys

from jaclang import jac_import
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.settings import settings
from jaclang.utils.test import TestCase


class TestDummy(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_needs_import_1(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True
        file_name = os.path.join(self.fixture_abs_path("./"), "needs_import_1.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen
        import jaclang.compiler.absyntree as ast

        ir = jac_file_to_pass(file_name, schedule=py_code_gen).ir
        self.assertEqual(len(ir.get_all_sub_nodes(ast.Architype)), 7)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("needs_import_1", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_1 imported", stdout_value)
        settings.py_raise = False

