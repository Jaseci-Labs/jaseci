"""Test pass module."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import JacImportPass
from jaclang.utils.test import TestCase


class ImportPassPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pygen_jac_cli(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base.jac"), JacImportPass)
        self.assertFalse(state.errors_had)
        self.assertIn("56", str(state.ir.to_dict()))

    def test_import_auto_impl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("autoimpl.jac"), JacImportPass)
        num_modules = len(state.ir.get_all_sub_nodes(ast.Module))
        mod_names = [i.name for i in state.ir.get_all_sub_nodes(ast.Module)]
        self.assertEqual(num_modules, 3)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_import_include_auto_impl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("incautoimpl.jac"), JacImportPass
        )
        num_modules = len(state.ir.get_all_sub_nodes(ast.Module))
        mod_names = [i.name for i in state.ir.get_all_sub_nodes(ast.Module)]
        self.assertEqual(num_modules, 4)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_annexalbe_by_discovery(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("incautoimpl.jac"), JacImportPass
        )
        for i in state.ir.get_all_sub_nodes(ast.Module):
            self.assertEqual(i.annexable_by, self.fixture_abs_path("autoimpl.jac"))
