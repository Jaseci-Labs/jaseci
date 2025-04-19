"""Test pass module."""

import io
import re
import sys

import jaclang.compiler.absyntree as ast
from jaclang.cli import cli
from jaclang.compiler.passes.main import JacImportPass
from jaclang.compiler.passes.main.fuse_typeinfo_pass import FuseTypeInfoPass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class ImportPassPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pygen_jac_cli(self) -> None:
        """Basic test for pass."""
        state = JacProgram.jac_file_to_pass(
            self.fixture_abs_path("base.jac"), JacImportPass
        )
        self.assertFalse(state.errors_had)
        self.assertIn("56", str(list(state.ir.jac_prog.modules.values())[1].to_dict()))

    def test_import_auto_impl(self) -> None:
        """Basic test for pass."""
        state = JacProgram.jac_file_to_pass(
            self.fixture_abs_path("autoimpl.jac"), JacImportPass
        )
        num_modules = len(list(state.ir.jac_prog.modules.values())[0].impl_mod)
        mod_names = [
            i.name for i in list(state.ir.jac_prog.modules.values())[0].impl_mod
        ]
        self.assertEqual(num_modules, 4)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_import_include_auto_impl(self) -> None:
        """Basic test for pass."""
        state = JacProgram.jac_file_to_pass(
            self.fixture_abs_path("incautoimpl.jac"), JacImportPass
        )
        # Adding 1 because of the included module it self
        # state.ir.jac_prog.modules is a dict and it will now contain two files
        #   incautoimpl.jac
        #   autoimpl.jac
        num_modules = len(list(state.ir.jac_prog.modules.values())[1].impl_mod) + 1
        mod_names = [
            i.name for i in list(state.ir.jac_prog.modules.values())[1].impl_mod
        ]
        self.assertEqual(num_modules, 5)
        self.assertEqual(
            "incautoimpl", list(state.ir.jac_prog.modules.values())[0].name
        )
        self.assertEqual("autoimpl", list(state.ir.jac_prog.modules.values())[1].name)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_annexalbe_by_discovery(self) -> None:
        """Basic test for pass."""
        state = JacProgram.jac_file_to_pass(
            self.fixture_abs_path("incautoimpl.jac"), JacImportPass
        )
        count = 0
        all_mods = state.ir.jac_prog.modules.values()
        self.assertEqual(len(all_mods), 2)
        for main_mod in all_mods:
            for i in main_mod.impl_mod:
                if i.name not in ["autoimpl", "incautoimpl"]:
                    count += 1
                    self.assertEqual(
                        i.annexable_by, self.fixture_abs_path("autoimpl.jac")
                    )
        self.assertEqual(count, 4)

    def test_py_raise_map(self) -> None:
        """Basic test for pass."""
        build = JacProgram.jac_file_to_pass(
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
            self.assertIn(i, build.ir.py_info.py_raise_map)
            self.assertRegex(
                re.sub(r".*fixtures/", "", build.ir.py_info.py_raise_map[i]).replace(
                    "\\", "/"
                ),
                p[i],
            )

    def test_py_raised_mods(self) -> None:
        """Basic test for pass."""
        state = JacProgram.jac_file_to_pass(
            self.fixture_abs_path("py_imp_test.jac"), schedule=py_code_gen_typed
        )
        for i in list(
            filter(
                lambda x: x.py_info.is_raised_from_py,
                state.ir.jac_prog.modules.values(),
            )
        ):
            print(ast.Module.get_href_path(i))

        module_count = len(
            list(
                filter(
                    lambda x: x.py_info.is_raised_from_py,
                    state.ir.jac_prog.modules.values(),
                )
            )
        )

        self.assertEqual(module_count, 8)

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
