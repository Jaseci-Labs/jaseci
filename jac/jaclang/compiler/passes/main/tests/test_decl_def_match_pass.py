"""Test pass module."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes.main import DeclImplMatchPass
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class DeclImplMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_parameter_count_mismatch(self) -> None:
        """Basic test for pass."""
        prog = JacProgram(main_file=self.fixture_abs_path("defn_decl_mismatch.jac"))
        state = prog.jac_file_to_pass(target=DeclImplMatchPass)

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
        for error in state.errors_had:
            errors_output += error.pretty_print() + "\n"

        for exp in expected_stdout_values:
            self.assertIn(exp, errors_output)

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        prog = JacProgram(main_file=self.fixture_abs_path("base.jac"))
        state = prog.jac_file_to_pass(target=DeclImplMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", prog.main_module.sym_tab.tab)
        self.assertIsNotNone(
            prog.main_module.sym_tab.tab["(o)Test.(c)say_hi"].decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", prog.main_module.sym_tab.tab)
        self.assertIsNotNone(
            prog.main_module.sym_tab.tab["(o)Test.(c)__init__"].decl.name_of.body
        )

    def test_ability_connected_to_decl_post(self) -> None:
        """Basic test for pass."""
        prog = JacProgram(main_file=self.fixture_abs_path("base2.jac"))
        state = prog.jac_file_to_pass(target=DeclImplMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", prog.main_module.sym_tab.tab)
        self.assertIsNotNone(
            prog.main_module.sym_tab.tab["(o)Test.(c)say_hi"].decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", prog.main_module.sym_tab.tab)
        self.assertIsNotNone(
            prog.main_module.sym_tab.tab["(o)Test.(c)__init__"].decl.name_of.body
        )

    def test_arch_ref_has_sym(self) -> None:
        """Basic test for pass."""
        prog = JacProgram(main_file=self.fixture_abs_path("defs_and_uses.jac"))
        prog.jac_file_to_pass(target=DeclImplMatchPass)
        for i in prog.main_module.get_all_sub_nodes(ast.ArchRef):
            self.assertIsNotNone(i.sym)

    def test_obj_hasvar_initialization(self) -> None:
        """Basic test for pass."""
        prog = JacProgram(main_file=self.fixture_abs_path("uninitialized_hasvars.jac"))
        state = prog.jac_file_to_pass(target=DeclImplMatchPass)
        self.assertTrue(state.errors_had)

        expected_stdout_values = (
            "Non default attribute 'var3' follows default attribute",
            "    4 |     has var1: int;",
            "    5 |     has var2: int = 42;",
            "    6 |     has var3: int; # <-- This should be syntax error.",
            "      |         ^^^^",
            "    7 | }",
            'Missing "postinit" method required by un initialized attribute(s).',
            "   11 | obj Test2 {",
            "   12 |     has var1: str;",
            "   13 |     has var2: int by postinit;",
            "      |         ^^^^",
            "   14 | }",
            "Non default attribute 'var4' follows default attribute",
            "   19 |     has var2: int = 42;",
            "   20 |     has var3: int by postinit;  # <-- This is fine.",
            "   21 |     has var4: int;  # <-- This should be syntax error.",
            "      |         ^^^^",
            "   22 |",
            "   23 |     can postinit() {",
        )

        errors_output = ""
        for error in state.errors_had:
            errors_output += error.pretty_print() + "\n"

        for exp in expected_stdout_values:
            self.assertIn(exp, errors_output)
