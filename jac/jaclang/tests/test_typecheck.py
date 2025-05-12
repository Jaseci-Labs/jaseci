"""Test Jac language generally."""

import io
import os
import sys
import unittest
import sysconfig
import tempfile
from unittest.mock import patch

from jaclang import JacMachineInterface as Jac, JacMachine
from jaclang.cli import cli
from jaclang.compiler.passes.main import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


@unittest.skip("Skipping typecheck tests")
class JacTypeCheckTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        self.mach = JacMachine(self.fixture_abs_path("./"))
        Jac.attach_program(
            self.mach,
            JacProgram(),
        )
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down test."""
        return super().tearDown()

    def test_multi_dim_arr_slice(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.tool(
            "ir",
            [
                "ast",
                self.fixture_abs_path("multi_dim_array_split.jac"),
            ],
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        expected_outputs = [
            "+-- AtomTrailer - Type: builtins.list[builtins.int]",
            "    +-- Name - arr - Type: builtins.list[builtins.list[builtins.int]],  SymbolTable: list",
            "+-- IndexSlice - [IndexSlice] - Type: builtins.list[builtins.list[builtins.int]],  SymbolTable: None",
            "        +-- Token - [, ",
            "        +-- Int - 1 - Type: Literal[1]?,  SymbolTable: None",
            "        +-- Token - :, ",
            "        +-- Int - 3 - Type: Literal[3]?,  SymbolTable: None",
            "        +-- Token - ,, ",
            "        +-- Int - 1 - Type: Literal[1]?,  SymbolTable: None",
            "        +-- Token - :, ",
            "        +-- Token - :, ",
            "        +-- Int - 2 - Type: Literal[2]?,  SymbolTable: None",
            "        +-- Token - ], ",
        ]

        for expected in expected_outputs:
            self.assertIn(expected, stdout_value)

    def test_needs_import_1(self) -> None:
        """Test py ast to Jac ast conversion output."""
        file_name = self.fixture_abs_path("pyfunc_1.py")

        from jaclang.compiler.passes.main.pyast_load_pass import PyastBuildPass
        import ast as py_ast
        import jaclang.compiler.unitree as uni

        with open(file_name, "r") as f:
            file_source = f.read()
            parsed_ast = py_ast.parse(file_source)
            try:
                py_ast_build_pass = PyastBuildPass(
                    ir_in=uni.PythonModuleAst(
                        parsed_ast, orig_src=uni.Source(file_source, file_name)
                    ),
                    prog=JacProgram(),
                ).ir_out
            except Exception as e:
                return f"Error While Jac to Py AST conversion: {e}"

        (prog := JacProgram()).compile_from_str(
            source_str=py_ast_build_pass.unparse(),
            file_path=file_name[:-3] + ".jac",
            mode=CMode.TYPECHECK,
        )

        architype_count = 0
        for mod in prog.mod.hub.values():
            if mod.name == "builtins":
                continue
            architype_count += len(mod.get_all_sub_nodes(uni.Architype))

        self.assertEqual(architype_count, 24)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(
            self.mach, "needs_import_1", base_path=self.fixture_abs_path("./")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_1 imported", stdout_value)

    def test_needs_import_2(self) -> None:
        """Test py ast to Jac ast conversion output."""
        file_name = self.fixture_abs_path("pyfunc_2.py")

        from jaclang.compiler.passes.main.pyast_load_pass import PyastBuildPass
        import ast as py_ast
        import jaclang.compiler.unitree as uni

        with open(file_name, "r") as f:
            file_source = f.read()
            parsed_ast = py_ast.parse(file_source)
            try:
                py_ast_build_pass = PyastBuildPass(
                    ir_in=uni.PythonModuleAst(
                        parsed_ast,
                        orig_src=uni.Source(file_source, file_name),
                    ),
                    prog=JacProgram(),
                ).ir_out
            except Exception as e:
                return f"Error While Jac to Py AST conversion: {e}"

            (prog := JacProgram()).compile_from_str(
                source_str=py_ast_build_pass.unparse(),
                file_path=file_name[:-3] + ".jac",
                mode=CMode.TYPECHECK,
            )

        architype_count = 0
        for mod in prog.mod.hub.values():
            if mod.name == "builtins":
                continue
            architype_count += len(mod.get_all_sub_nodes(uni.Architype))

        self.assertEqual(architype_count, 30)  # Because of the Architype from math
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(
            self.mach, "needs_import_2", base_path=self.fixture_abs_path("./")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_2 imported", stdout_value)
        self.assertEqual(stdout_value.count("<class 'bytes'>"), 3)

    def test_needs_import_3(
        self,
    ) -> None:  # TODO : Pyfunc_3 has a bug in conversion in matchmapping node
        """Test py ast to Jac ast conversion output."""
        file_name = self.fixture_abs_path("pyfunc_3.py")
        import jaclang.compiler.unitree as uni

        with open(file_name, "r") as f:
            file_source = f.read()
        (prog := JacProgram()).compile_from_str(
            source_str=file_source, file_path=file_name, mode=CMode.TYPECHECK
        )

        architype_count = sum(
            len(mod.get_all_sub_nodes(uni.Architype))
            for mod in prog.mod.hub.values()
            if mod.name != "builtins"
        )
        self.assertEqual(
            architype_count, 58
        )  # Fixed duplication of 'case' module (previously included 3 times, added 20 extra Architypes; 75 → 55)
        builtin_mod = next(
            (mod for name, mod in prog.mod.hub.items() if "builtins" in name),
            None,
        )
        self.assertEqual(len(builtin_mod.get_all_sub_nodes(uni.Architype)), 109)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(
            self.mach, "needs_import_3", base_path=self.fixture_abs_path("./")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_3 imported", stdout_value)

    def test_type_fuse_expr(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.tool(
            "ir",
            [
                "ast",
                self.examples_abs_path("reference/collection_values.jac"),
            ],
        )

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            "builtins.dict[builtins.int, builtins.int]",
            stdout_value,
        )
        self.assertIn(
            "typing.Generator[builtins.int, None, None]",
            stdout_value,
        )

    def test_random_check(self) -> None:
        """Test py ast to Jac ast conversion output."""
        from jaclang.settings import settings

        module_paths = ["random", "ast"]
        for module_path in module_paths:
            stdlib_dir = sysconfig.get_paths()["stdlib"]
            file_path = os.path.join(
                stdlib_dir,
                module_path + ".py",
            )
            settings.print_py_raised_ast = True
            with open(file_path) as f:
                file_source = f.read()
            ir = JacProgram().compile_from_str(
                source_str=file_source,
                file_path=file_path,
                mode=CMode.TYPECHECK,
            )
            gen_ast = ir.pp()
            if module_path == "random":
                self.assertIn("ModulePath - statistics -", gen_ast)
            else:
                self.assertIn("+-- Name - NodeTransformer - Type: No", gen_ast)

    def test_deep_convert(self) -> None:
        """Test py ast to Jac ast conversion output."""
        file_name = self.fixture_abs_path("pyfunc_1.py")

        import jaclang.compiler.unitree as uni
        from jaclang.settings import settings

        settings.print_py_raised_ast = True
        with open(file_name, "r") as f:
            file_source = f.read()
        ir = (prog := JacProgram()).compile_from_str(
            source_str=file_source, file_path=file_name, mode=CMode.TYPECHECK
        )
        jac_ast = ir.pp()
        self.assertIn(" |   +-- String - 'Loop completed normally{}'", jac_ast)
        sub_node_list_count = 0
        for i in prog.mod.hub.values():
            if i.name == "builtins":
                continue
            sub_node_list_count += len(i.get_all_sub_nodes(uni.SubNodeList))
        self.assertEqual(sub_node_list_count, 623)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(self.mach, "deep_convert", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Deep convo is imported", stdout_value)

    def test_ds_type_check_pass(self) -> None:
        """Test conn assign on edges."""
        (mypass := JacProgram()).compile(
            self.examples_abs_path("micro/simple_walk.jac"),
            mode=CMode.TYPECHECK,
        )
        self.assertEqual(len(mypass.errors_had), 0)
        self.assertEqual(len(mypass.warnings_had), 0)

    def test_ds_type_check_pass2(self) -> None:
        """Test conn assign on edges."""
        (mypass := JacProgram()).compile(
            self.examples_abs_path("guess_game/guess_game5.jac"),
            mode=CMode.TYPECHECK,
        )
        self.assertEqual(len(mypass.errors_had), 0)
        self.assertEqual(len(mypass.warnings_had), 0)

    def test_circle_override1_type_check_pass(self) -> None:
        """Test conn assign on edges."""
        (mypass := JacProgram()).compile(
            self.examples_abs_path("manual_code/circle.jac"),
            mode=CMode.TYPECHECK,
        )
        self.assertEqual(len(mypass.errors_had), 0)
        # FIXME: Figure out what to do with warning.
        # self.assertEqual(len(mypass.warnings_had), 0)

    def test_expr_types(self) -> None:
        """Testing for print AstTool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cli.tool("ir", ["ast", f"{self.fixture_abs_path('expr_type.jac')}"])

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        self.assertRegex(
            stdout_value, r"4\:9 \- 4\:14.*BinaryExpr \- Type\: builtins.int"
        )
        self.assertRegex(
            stdout_value, r"7\:9 \- 7\:17.*FuncCall \- Type\: builtins.float"
        )
        self.assertRegex(
            stdout_value, r"9\:6 \- 9\:11.*CompareExpr \- Type\: builtins.bool"
        )
        self.assertRegex(
            stdout_value, r"10\:6 - 10\:15.*BinaryExpr \- Type\: builtins.str"
        )
        self.assertRegex(
            stdout_value, r"11\:5 \- 11\:13.*AtomTrailer \- Type\: builtins.int"
        )
        self.assertRegex(
            stdout_value, r"12\:5 \- 12\:14.*UnaryExpr \- Type\: builtins.bool"
        )
        self.assertRegex(
            stdout_value, r"13\:5 \- 13\:25.*IfElseExpr \- Type\: Literal\['a']\?"
        )
        self.assertRegex(
            stdout_value,
            r"14\:5 \- 14\:27.*ListCompr - \[ListCompr] \- Type\: builtins.list\[builtins.int]",
        )

    def test_type_check(self) -> None:
        """Testing for print AstTool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.check(f"{self.fixture_abs_path('game1.jac')}")
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Errors: 0, Warnings: 1", stdout_value)
