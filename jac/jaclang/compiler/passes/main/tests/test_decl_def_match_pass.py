"""Test pass module."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import DeclImplMatchPass
from jaclang.utils.test import TestCase


class DeclImplMatchPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_parameter_count_mismatch(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("defn_decl_mismatch.jac"), DeclImplMatchPass
        )

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

    def test_parameter_name_mismatch(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("defn_decl_mismatch.jac"), DeclImplMatchPass
        )

        expected_stdout_values = (
            "Parameter name mismatch for ability (o)SomeObj.(c)bar.",
            "   14 |",
            "   15 | # Mis matching parameter name.",
            "   16 | :obj:SomeObj:can:bar(param1: str, praam2:int) -> str {",
            "      |                                   ^^^^^^",
            '   17 |     return "bar";',
            "   18 | }",
            "From the declaration of bar.",
            "    3 | obj SomeObj {",
            "    4 |     can foo(param1: str, param2:int) -> str;",
            "    5 |     can bar(param1: str, param2:int) -> str;",
            "      |                          ^^^^^^",
            "    6 | }",
        )

        errors_output = ""
        for error in state.errors_had:
            errors_output += error.pretty_print() + "\n"

        for exp in expected_stdout_values:
            self.assertIn(exp, errors_output)

    def test_ability_connected_to_decl(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("base.jac"), DeclImplMatchPass)
        self.assertFalse(state.errors_had)
        self.assertIn("(o)Test.(c)say_hi", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)say_hi"].decl.name_of.body
        )
        self.assertIn("(o)Test.(c)__init__", state.ir.sym_tab.tab)
        self.assertIsNotNone(
            state.ir.sym_tab.tab["(o)Test.(c)__init__"].decl.name_of.body
        )

    def test_obj_hasvar_initialization(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("uninitialized_hasvars.jac"), DeclImplMatchPass
        )
        self.assertTrue(state.errors_had)

        expected_stdout_values = (
            "Non default attribute 'var3' follows default attribute",
            "    4 |     has var1: int;",
            "    5 |     has var2: int = 42;",
            "    6 |     has var3: int; # <-- This should be syntax error.",
            "      |         ~~~~",
            "    7 | }",
            'Non default attribute(s) "var2", "var3" are not initialized in the init method.',
            "   14 |     has var4: int = 42;",
            "   15 |",
            '   16 |     can init() {  # <-- Should be error because "var2", "var3" are not initialized.',
            "      |         ~~~~",
            "   17 |         self.var1 = 1;",
            "   18 |     }",
            'Non default attribute(s) "var2", "var3" are not initialized in the init method.',
            "   26 |     has var4: int = 42;",
            "   27 |",
            "   28 |     can init();",
            "      |         ~~~~",
            "   29 | }",
            'Missing "postinit" method required by un initialized attribute(s).',
            "   36 | obj Test4 {",
            "   37 |     has var1: str;",
            "   38 |     has var2: int by postinit;",
            "      |         ~~~~",
            "   39 | }",
            'Non default attribute(s) "var2" are not initialized in the postinit method.',
            "   44 |     has var2: int by postinit;",
            "   45 |",
            "   46 |     can postinit() {",
            "      |         ~~~~~~~~",
            "   47 |     }",
            "   48 | }",
            "Non default attribute 'var4' follows default attribute",
            "   53 |     has var2: int = 42;",
            "   54 |     has var3: int by postinit;  # <-- This is fine.",
            "   55 |     has var4: int;  # <-- This should be syntax error.",
            "      |         ~~~~",
            "   56 |",
            "   57 |     can postinit() {",
        )

        errors_output = ""
        for error in state.errors_had:
            errors_output += error.pretty_print() + "\n"

        for exp in expected_stdout_values:
            self.assertIn(exp, errors_output)

    def test_arch_ref_has_sym(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            self.fixture_abs_path("defs_and_uses.jac"), DeclImplMatchPass
        )
        for i in state.ir.get_all_sub_nodes(ast.ArchRef):
            self.assertIsNotNone(i.sym)
