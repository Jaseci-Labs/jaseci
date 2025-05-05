"""Test pass module."""

import io
import sys

import jaclang.compiler.unitree as uni
from jaclang import JacMachine as Jac
from jaclang.cli import cli
from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.machinestate import JacMachineState
from jaclang.utils.test import TestCase


class DeclImplMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        self.mach = JacMachineState(self.fixture_abs_path("./"))
        Jac.attach_program(
            self.mach,
            JacProgram(),
        )
        return super().setUp()

    def test_parameter_count_mismatch(self) -> None:
        """Basic test for pass."""
        (out := JacProgram()).compile(self.fixture_abs_path("defn_decl_mismatch.jac"))

        expected_stdout_values = (
            "Parameter count mismatch for ability (o)SomeObj.(c)foo.",
            "    8 |",
            "    9 | # Miss match parameter count.",
            "   10 | :obj:SomeObj:can:foo(param1: str) -> str {",
            "      | ^^^^^^^^^^^^^^^^^^^^",
            '   11 |     return "foo";',
            "   12 | }",
            "From the declaration of foo.",
            "    2 |",
            "    3 | obj SomeObj {",
            "    4 |     can foo(param1: str, param2:int) -> str;",
            "      |         ^^^",
            "    5 |     can bar(param1: str, param2:int) -> str;",
            "    6 | }",
        )

        errors_output = ""
        for error in out.errors_had:
            errors_output += error.pretty_print() + "\n"

        for exp in expected_stdout_values:
            self.assertIn(exp, errors_output)

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = (out := JacProgram()).compile(self.fixture_abs_path("base.jac"))
        self.assertFalse(out.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.impl_mod[0].sym_tab.names_in_scope)
        self.assertIsNotNone(
            state.impl_mod[0]
            .sym_tab.names_in_scope["(o)Test.(c)say_hi"]
            .decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", state.impl_mod[0].sym_tab.names_in_scope)
        self.assertIsNotNone(
            state.impl_mod[0]
            .sym_tab.names_in_scope["(o)Test.(c)__init__"]
            .decl.name_of.body
        )

    def test_ability_connected_to_decl_post(self) -> None:
        """Basic test for pass."""
        state = (out := JacProgram()).compile(self.fixture_abs_path("base2.jac"))
        self.assertFalse(out.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.sym_tab.impl_mod[0].names_in_scope)
        self.assertIsNotNone(
            state.sym_tab.impl_mod[0]
            .names_in_scope["(o)Test.(c)say_hi"]
            .decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", state.impl_mod[0].sym_tab.names_in_scope)
        self.assertIsNotNone(
            state.impl_mod[0]
            .sym_tab.names_in_scope["(o)Test.(c)__init__"]
            .decl.name_of.body
        )

    def test_run_base2(self) -> None:
        """Test that the walker and node can be created dynamically."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.run(self.fixture_abs_path("base2.jac"))
        output = captured_output.getvalue().strip()
        self.assertIn("56", output)

    def test_arch_ref_has_sym(self) -> None:
        """Basic test for pass."""
        state = JacProgram().compile(self.fixture_abs_path("defs_and_uses.jac"))
        for i in state.get_all_sub_nodes(uni.ArchRef):
            self.assertIsNotNone(i.sym)

    def test_single_impl_annex(self) -> None:
        """Basic test for pass."""
        mypass = JacProgram().compile(
            self.examples_abs_path("manual_code/circle_pure.jac")
        )
        self.assertEqual(
            mypass.impl_mod[0].pp().count("AbilityDef - (o)Circle.(c)area"), 1
        )

    def test_impl_decl_resolution_fix(self) -> None:
        """Test walking through edges and nodes."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(self.mach, "mtest", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("2.0\n", stdout_value)

    def test_impl_grab(self) -> None:
        """Test walking through edges."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(self.mach, "impl_grab", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("1.414", stdout_value)

    def test_nested_impls(self) -> None:
        """Test complex nested impls."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Jac.jac_import(self.mach, "nested_impls", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertIn("Hello,from bar in kk", stdout_value[0])
        self.assertIn("Greeting: Hello, World!", stdout_value[1])
        self.assertIn("Repeated: Hello", stdout_value[2])
        self.assertIn("Hello, World!", stdout_value[3])
        self.assertIn("Last message:!", stdout_value[4])
        self.assertIn("Final message:!", stdout_value[5])
