"""Test ast build pass module."""
import inspect
from copy import copy

from jaclang.jac.passes.blue_pygen_pass import BluePygenPass
from jaclang.jac.transpiler import transpile_jac_file
from jaclang.jac.utils import get_ast_nodes_as_snake_case as ast_snakes
from jaclang.utils.test import TestCaseMicroSuite


class BluePygenPassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pygen_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = transpile_jac_file(
            self.fixture_abs_path("../../../../cli/jac_cli.jac")
        )
        print(code_gen)
        self.assertGreater(len(code_gen), 200)

    def test_no_typo_in_pass(self) -> None:
        """Test for enter/exit name diffs with parser."""
        ast_func_names = [
            x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
        ]
        pygen_func_names = copy(BluePygenPass.marked_incomplete)
        for name, value in inspect.getmembers(BluePygenPass):
            if (
                (name.startswith("enter_") or name.startswith("exit_"))
                and inspect.isfunction(value)
                and not getattr(BluePygenPass.__base__, value.__name__, False)
                and value.__qualname__.split(".")[0]
                == BluePygenPass.__name__.replace("enter_", "").replace("exit_", "")
            ):
                pygen_func_names.append(name.replace("enter_", "").replace("exit_", ""))
        for name in pygen_func_names:
            self.assertIn(name, ast_func_names)

    def test_pass_ast_complete(self) -> None:
        """Test for enter/exit name diffs with parser."""
        ast_func_names = [
            x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
        ]
        pygen_func_names = copy(BluePygenPass.marked_incomplete)
        for name, value in inspect.getmembers(BluePygenPass):
            if (
                (name.startswith("enter_") or name.startswith("exit_"))
                and inspect.isfunction(value)
                and not getattr(BluePygenPass.__base__, value.__name__, False)
                and value.__qualname__.split(".")[0]
                == BluePygenPass.__name__.replace("enter_", "").replace("exit_", "")
            ):
                pygen_func_names.append(name.replace("enter_", "").replace("exit_", ""))
        for name in ast_func_names:
            self.assertIn(name, pygen_func_names)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = transpile_jac_file(filename)
        self.assertGreater(len(code_gen), 10)


BluePygenPassTests.self_attach_micro_tests()
