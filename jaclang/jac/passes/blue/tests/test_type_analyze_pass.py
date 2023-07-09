"""Test type analyze pass module."""
import inspect

from jaclang.jac.passes.blue import BluePygenPass, TypeAnalyzePass
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.jac.utils import get_ast_nodes_as_snake_case as ast_snakes
from jaclang.utils.test import TestCaseMicroSuite


class TypeAnalyzePassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pygen_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../cli/cli.jac"), target=BluePygenPass
        )
        # print(code_gen.ir.meta["py_code"])
        self.assertFalse(code_gen.errors_had)
        self.assertGreater(len(code_gen.ir.meta["py_code"]), 200)

    def test_pass_ast_complete(self) -> None:
        """Test for enter/exit name diffs with parser."""
        ast_func_names = [
            x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
        ]
        pygen_func_names = []
        for name, value in inspect.getmembers(TypeAnalyzePass):
            if (
                (name.startswith("enter_") or name.startswith("exit_"))
                and inspect.isfunction(value)
                and not getattr(TypeAnalyzePass.__base__, value.__name__, False)
                and value.__qualname__.split(".")[0]
                == TypeAnalyzePass.__name__.replace("enter_", "").replace("exit_", "")
            ):
                pygen_func_names.append(name.replace("enter_", "").replace("exit_", ""))
        for name in pygen_func_names:
            self.assertIn(name, ast_func_names)
        for name in ast_func_names:
            self.assertIn(name, pygen_func_names)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        ast = jac_file_to_pass(filename, "", target=BluePygenPass).ir
        typed_ast = TypeAnalyzePass(mod_path=filename, input_ir=ast).ir
        self.assertGreater(len(str(typed_ast.to_dict())), 10)


TypeAnalyzePassTests.self_attach_micro_tests()
