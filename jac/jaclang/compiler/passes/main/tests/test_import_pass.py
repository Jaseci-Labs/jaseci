"""Test pass module."""

import io
import re
import sys

import jaclang.compiler.unitree as uni
from jaclang.cli import cli
from jaclang.compiler.passes.main.schedules import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class ImportPassPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pygen_jac_cli(self) -> None:
        """Basic test for pass."""
        (out := JacProgram()).compile(self.fixture_abs_path("base.jac"))
        self.assertFalse(out.errors_had)
        mod = out.mod.hub[self.fixture_abs_path("impl/imps.jac")]
        self.assertIn("56", str(mod.to_dict()))

    def test_import_auto_impl(self) -> None:
        """Basic test for pass."""
        (prog := JacProgram()).compile(self.fixture_abs_path("autoimpl.jac"))
        num_modules = len(list(prog.mod.hub.values())[0].impl_mod)
        mod_names = [i.name for i in list(prog.mod.hub.values())[0].impl_mod]
        self.assertEqual(num_modules, 4)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_import_include_auto_impl(self) -> None:
        """Basic test for pass."""
        (prog := JacProgram()).compile(self.fixture_abs_path("incautoimpl.jac"))
        num_modules = len(list(prog.mod.hub.values())[1].impl_mod) + 1
        mod_names = [i.name for i in list(prog.mod.hub.values())[1].impl_mod]
        self.assertEqual(num_modules, 5)
        self.assertEqual("incautoimpl", list(prog.mod.hub.values())[0].name)
        self.assertEqual("autoimpl", list(prog.mod.hub.values())[1].name)
        self.assertIn("getme.impl", mod_names)
        self.assertIn("autoimpl.impl", mod_names)
        self.assertIn("autoimpl.something.else.impl", mod_names)

    def test_annexalbe_by_discovery(self) -> None:
        """Basic test for pass."""
        (prog := JacProgram()).compile(self.fixture_abs_path("incautoimpl.jac"))
        count = 0
        all_mods = prog.mod.hub.values()
        self.assertEqual(len(all_mods), 6)
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
        (build := JacProgram()).compile(
            self.fixture_abs_path("py_imp_test.jac"),
            mode=CMode.TYPECHECK,
        )
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
            self.assertIn(i, build.py_raise_map)
            self.assertRegex(
                re.sub(r".*fixtures/", "", build.py_raise_map[i]).replace("\\", "/"),
                p[i],
            )

    def test_py_raised_mods(self) -> None:
        """Basic test for pass."""
        (prog := JacProgram()).compile(
            self.fixture_abs_path("py_imp_test.jac"), mode=CMode.TYPECHECK
        )
        for i in list(
            filter(
                lambda x: x.py_info.is_raised_from_py,
                prog.mod.hub.values(),
            )
        ):
            print(uni.Module.get_href_path(i))

        module_count = len(
            list(
                filter(
                    lambda x: x.py_info.is_raised_from_py,
                    prog.mod.hub.values(),
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

    def test_raise_syntax_error(self) -> None:
        """Test raise error on the parser , dont go to the next pass."""
        (state := JacProgram()).compile(self.fixture_abs_path("main_err.jac"))
        self.assertTrue(state.errors_had)
        self.assertEqual(len(state.errors_had), 1)
        self.assertIn("Syntax Error", state.errors_had[0].msg)
