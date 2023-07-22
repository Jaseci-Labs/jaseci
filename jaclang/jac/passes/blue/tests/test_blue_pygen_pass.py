"""Test ast build pass module."""
import inspect

from jaclang.jac.passes.blue import BluePygenPass
from jaclang.jac.transpiler import jac_file_to_pass, transpile_jac_blue
from jaclang.jac.utils import get_ast_nodes_as_snake_case as ast_snakes
from jaclang.utils.test import TestCaseMicroSuite


class BluePygenPassTests(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../cli/cli.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)

    def test_pipe_operator(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn(
            'say((dump(print(len)))({"name": "value"}))', code_gen.ir.meta["py_code"]
        )
        self.assertIn(
            '{"name": "value"}(len(print(print(print))))', code_gen.ir.meta["py_code"]
        )
        self.assertIn("a = (5 + 10) * 2", code_gen.ir.meta["py_code"])

    def test_atomic_pipe_operator(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn(
            'say((dump(print)(len))({"name": "value"}))', code_gen.ir.meta["py_code"]
        )

    def test_pipe_operator_multi_param(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn("self.func(*args, **kwargs)", code_gen.ir.meta["py_code"])
        self.assertIn("inspect.signature(func)", code_gen.ir.meta["py_code"])
        self.assertIn("self.registry.items()", code_gen.ir.meta["py_code"])

    def test_with_stmt(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn(
            'with open("file.txt") as f, open("file2.txt") as f:',
            code_gen.ir.meta["py_code"],
        )

    def test_empty_codeblock(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn("pass", code_gen.ir.meta["py_code"])

    def test_enum_gen(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("codegentext.jac"), target=BluePygenPass
        )
        self.assertFalse(code_gen.errors_had)
        self.assertIn(
            "from enum import Enum as __jac_Enum__, auto as __jac_auto__",
            code_gen.ir.meta["py_code"],
        )
        self.assertIn("class Color(__jac_Enum__):", code_gen.ir.meta["py_code"])
        self.assertIn("GREEN = __jac_auto__()", code_gen.ir.meta["py_code"])
        self.assertIn("RED = 1", code_gen.ir.meta["py_code"])

    def test_pass_ast_complete(self) -> None:
        """Test for enter/exit name diffs with parser."""
        ast_func_names = [
            x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
        ]
        pygen_func_names = []
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
        for name in ast_func_names:
            self.assertIn(name, pygen_func_names)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = transpile_jac_blue(filename, "")
        self.assertGreater(len(code_gen), 10)


BluePygenPassTests.self_attach_micro_tests()
