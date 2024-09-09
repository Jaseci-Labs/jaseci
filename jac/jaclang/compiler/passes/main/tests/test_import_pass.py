"""Test pass module."""

import io
import re
import sys

import jaclang.compiler.absyntree as ast
from jaclang.cli import cli
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import JacImportPass
from jaclang.compiler.passes.main.fuse_typeinfo_pass import FuseTypeInfoPass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
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
        self.assertEqual(num_modules, 4)
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
        self.assertEqual(num_modules, 5)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_annexalbe_by_discovery(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("incautoimpl.jac"), JacImportPass
        )
        count = 0
        for i in state.ir.get_all_sub_nodes(ast.Module):
            if i.name != "autoimpl":
                count += 1
                self.assertEqual(i.annexable_by, self.fixture_abs_path("autoimpl.jac"))
        self.assertEqual(count, 4)

    def test_py_raise_map(self) -> None:
        """Basic test for pass."""
        build = jac_file_to_pass(
            self.fixture_abs_path("py_imp_test.jac"),
            FuseTypeInfoPass,
            schedule=py_code_gen_typed,
        )
        assert isinstance(build.ir, ast.Module)
        p = {
            "math": r"jaclang/vendor/mypy/typeshed/stdlib/math.pyi$",
            "pygame_mock": r"pygame_mock/__init__.pyi$",
            "pygame_mock.color": r"pygame_mock/color.py$",
            "pygame_mock.constants": r"pygame_mock/constants.py$",
            "argparse": r"jaclang/vendor/mypy/typeshed/stdlib/argparse.pyi$",
            "builtins": r"jaclang/vendor/mypy/typeshed/stdlib/builtins.pyi$",
            "pygame_mock.display": r"pygame_mock/display.py$",
            "os": r"jaclang/vendor/mypy/typeshed/stdlib/os/__init__.pyi$",
            "genericpath": r"jaclang/vendor/mypy/typeshed/stdlib/genericpath.pyi$",
        }
        for i in p:
            self.assertIn(i, build.ir.py_raise_map)
            self.assertRegex(re.sub(r".*fixtures/", "", build.ir.py_raise_map[i]), p[i])

    def test_py_raised_mods(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("py_imp_test.jac"), schedule=py_code_gen_typed
        )
        self.assertEqual(
            len(
                list(
                    filter(
                        lambda x: x.is_raised_from_py,
                        state.ir.get_all_sub_nodes(ast.Module),
                    )
                )
            ),
            7,
        )

    # def test_py_resolve_list(self) -> None:
    #     """Basic test for pass."""
    #     state: JacImportPass = jac_file_to_pass(
    #         self.examples_abs_path("rpg_game/jac_impl/jac_impl_5/main.jac"),
    #         JacImportPass,
    #     )
    #     self.assertGreater(len(state.py_resolve_list), 20)
    #     self.assertIn("pygame.sprite.Sprite.__init__", state.py_resolve_list)
    #     self.assertIn("pygame.mouse.get_pressed", state.py_resolve_list)
    #     self.assertIn("pygame.K_SPACE", state.py_resolve_list)
    #     self.assertIn("random.randint", state.py_resolve_list)
    #     self.assertIn("pygame.font.Font", state.py_resolve_list)

    def test_double_empty_anx(self) -> None:
        """Test importing python."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.run(self.fixture_abs_path("autoimpl.jac"))
        cli.run(self.fixture_abs_path("autoimpl.jac"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("foo", stdout_value)
        self.assertIn("bar", stdout_value)
        self.assertIn("baz", stdout_value)
