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

    def test_circle_py_ast(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../../examples/manual_code/circle.jac"),
            target=PyastGenPass,
        )
        # import ast as ast3
        # if isinstance(code_gen.ir.gen.py_ast, ast3.AST):
        #     print(ast3.dump(code_gen.ir.gen.py_ast, indent=2))
        #     print(ast3.unparse(code_gen.ir.gen.py_ast))
        self.assertFalse(code_gen.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyastGenPass
        )
        self.assertGreater(len(code_gen.ir.gen.py), 10)


PyastGenPassTests.self_attach_micro_tests()
