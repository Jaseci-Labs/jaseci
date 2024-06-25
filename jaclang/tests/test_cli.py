"""Test Jac cli module."""

import inspect
import io
import os
import subprocess
import sys

from jaclang.cli import cli
from jaclang.plugin.builtin import dotgen
from jaclang.utils.test import TestCase


class JacCliTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli_run(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.fixture_abs_path("hello.jac"))

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        self.assertIn("Hello World!", stdout_value)

    def test_jac_cli_alert_based_err(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        # Execute the function
        # try:
        cli.enter(self.fixture_abs_path("err2.jac"), entrypoint="speak", args=[])  # type: ignore
        # except Exception as e:
        #     print(f"Error: {e}")

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdout_value = captured_output.getvalue()
        # print(stdout_value)
        self.assertIn("Errors occurred", stdout_value)

    def test_jac_ast_tool_pass_template(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cli.tool("pass_template")

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Sub objects.", stdout_value)
        self.assertGreater(stdout_value.count("def exit_"), 10)

    def test_jac_cmd_line(self) -> None:
        """Basic test for pass."""
        process = subprocess.Popen(
            ["jac"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout_value, _ = process.communicate(input="exit\n")
        self.assertEqual(process.returncode, 0, "Process did not exit successfully")
        self.assertIn("Welcome to the Jac CLI!", stdout_value)

    def test_ast_print(self) -> None:
        """Testing for print AstTool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cli.tool("ir", ["ast", f"{self.fixture_abs_path('hello.jac')}"])

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("+-- Token", stdout_value)

    def test_ast_dotgen(self) -> None:
        """Testing for print AstTool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        cli.tool("ir", ["ast.", f"{self.fixture_abs_path('hello.jac')}"])

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn('[label="MultiString"]', stdout_value)

    def test_type_check(self) -> None:
        """Testing for print AstTool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.check(f"{self.fixture_abs_path('game1.jac')}")
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Errors: 0, Warnings: 1", stdout_value)

    def test_type_info(self) -> None:
        """Testing for type info inside the ast tool."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.tool("ir", ["ast", f"{self.fixture_abs_path('type_info.jac')}"])
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.count("type_info.ServerWrapper"), 7)
        self.assertEqual(stdout_value.count("builtins.int"), 2)
        self.assertEqual(stdout_value.count("builtins.str"), 7)

    def test_build_and_run(self) -> None:
        """Testing for print AstTool."""
        if os.path.exists(f"{self.fixture_abs_path('needs_import.jir')}"):
            os.remove(f"{self.fixture_abs_path('needs_import.jir')}")
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.build(f"{self.fixture_abs_path('needs_import.jac')}")
        cli.run(f"{self.fixture_abs_path('needs_import.jir')}")
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Errors: 0, Warnings: 0", stdout_value)
        self.assertIn("<module 'pyfunc' from", stdout_value)

    def test_cache_no_cache_on_run(self) -> None:
        """Basic test for pass."""
        process = subprocess.Popen(
            ["jac", "run", f"{self.fixture_abs_path('hello_nc.jac')}", "-nc"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = process.communicate()
        self.assertFalse(
            os.path.exists(
                f"{self.fixture_abs_path(os.path.join('__jac_gen__', 'hello_nc.jbc'))}"
            )
        )
        self.assertIn("Hello World!", stdout)
        process = subprocess.Popen(
            ["jac", "run", f"{self.fixture_abs_path('hello_nc.jac')}", "-c"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = process.communicate()
        self.assertIn("Hello World!", stdout)
        self.assertTrue(
            os.path.exists(
                f"{self.fixture_abs_path(os.path.join('__jac_gen__', 'hello_nc.jbc'))}"
            )
        )
        os.remove(
            f"{self.fixture_abs_path(os.path.join('__jac_gen__', 'hello_nc.jbc'))}"
        )

    def test_run_test(self) -> None:
        """Basic test for pass."""
        process = subprocess.Popen(
            ["jac", "test", f"{self.fixture_abs_path('run_test.jac')}", "-m 2"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        self.assertIn("Ran 3 tests", stderr)
        self.assertIn("FAILED (failures=2)", stderr)
        self.assertIn("F.F", stderr)

        process = subprocess.Popen(
            [
                "jac",
                "test",
                "-d" + f"{self.fixture_abs_path('../../../')}",
                "-f" + "circle*",
                "-x",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        self.assertIn("circle", stdout)
        self.assertNotIn("circle_purfe.test", stdout)
        self.assertNotIn("circle_pure.impl", stdout)

        process = subprocess.Popen(
            ["jac", "test", "-f" + "*run_test.jac", "-m 3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        self.assertIn("...F", stderr)
        self.assertIn("F.F", stderr)

    def test_graph_coverage(self) -> None:
        """Test for coverage of graph cmd."""
        graph_params = set(inspect.signature(cli.dot).parameters.keys())
        dotgen_params = set(inspect.signature(dotgen).parameters.keys())
        dotgen_params = dotgen_params - {"node", "dot_file", "edge_type"}
        dotgen_params.update({"initial", "saveto", "connection", "session"})
        self.assertTrue(dotgen_params.issubset(graph_params))
        self.assertEqual(len(dotgen_params) + 1, len(graph_params))

    def test_graph(self) -> None:
        """Test for graph CLI cmd."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.dot(
            f"{self.fixture_abs_path('../../../examples/reference/connect_expressions.jac')}"
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        if os.path.exists("connect_expressions.dot"):
            os.remove("connect_expressions.dot")
        self.assertIn("11\n13\n15\n>>> Graph content saved to", stdout_value)
        self.assertIn("connect_expressions.dot\n", stdout_value)

    def test_py_to_jac(self) -> None:
        """Test for graph CLI cmd."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.py2jac(f"{self.fixture_abs_path('../../tests/fixtures/pyfunc.py')}")
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("can my_print(x: object) -> None", stdout_value)
