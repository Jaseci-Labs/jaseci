"""Test ast build pass module."""
from jaclang.jac.passes.blue import PyastGenPass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class PyastGenPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = PyastGenPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../cli/cli.jac"), target=PyastGenPass
        )
        self.assertFalse(code_gen.errors_had)

    def test_hodge_podge(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../../examples/micro/hodge_podge.jac"),
            target=PyastGenPass,
        )
        # import ast as ast3

        # if isinstance(code_gen.ir.gen.py_ast, ast3.AST):
        #     print(ast3.dump(code_gen.ir.gen.py_ast, indent=2))
        #     print(ast3.unparse(code_gen.ir.gen.py_ast))
        #     exec(compile(code_gen.ir.gen.py_ast, "<string>", "exec"))
        self.assertFalse(code_gen.errors_had)

    def test_circle_py_ast(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../../examples/manual_code/circle.jac"),
            target=PyastGenPass,
        )
        # import ast as ast3

        # if isinstance(code_gen.ir.gen.py_ast, ast3.AST):
        #     from_jac = ast3.dump(code_gen.ir.gen.py_ast, indent=2)
        #     back_to_py = ast3.unparse(code_gen.ir.gen.py_ast)
        #     from_py = ast3.dump(ast3.parse(back_to_py), indent=2)
        #     print(back_to_py)
        #     # print(from_jac, "\n\n", from_py)
        #     # print(ast3.dump(code_gen.ir.gen.py_ast, indent=2))
        #     # print(ast3.unparse(code_gen.ir.gen.py_ast))
        #     prog = compile(code_gen.ir.gen.py_ast, "<string>", "exec")
        #     exec(prog)
        self.assertFalse(code_gen.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyastGenPass
        )
        self.assertGreater(len(code_gen.ir.gen.py), 10)


PyastGenPassTests.self_attach_micro_tests()
