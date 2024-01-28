"""Test ast build pass module."""
import os

import jaclang
from jaclang.utils.helpers import extract_headings, heading_to_snake
from jaclang.utils.lang_tools import AstTool
from jaclang.utils.test import TestCase


class JacFormatPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_pass_template(self) -> None:
        """Basic test for pass."""
        out = AstTool().pass_template()
        self.assertIn("target: Expr,", out)
        self.assertIn("self, node: ast.ReturnStmt", out)
        self.assertIn("exprs: SubNodeList[ExprAsItem],", out)
        self.assertIn("value: str,", out)
        self.assertIn("def exit_module(self, node: ast.Module)", out)
        self.assertGreater(out.count("def exit_"), 20)

    def test_gendotfile(self) -> None:
        """Testing for HTML entity."""
        current_directory = os.getcwd()
        for root, _, files in os.walk(current_directory):
            for jac_file in files:
                if jac_file.endswith(".jac"):
                    jac_file_path = os.path.join(root, jac_file)
                    out = AstTool().dot_gen([jac_file_path])
                    forbidden_strings = ["<<", ">>", "<init>", "<super>"]
                    for i in forbidden_strings:
                        self.assertNotIn(i, out)

    def test_print(self) -> None:
        """Testing for print AstTool."""
        jac_directory = os.path.join(
            os.path.dirname(jaclang.__file__), "../examples/reference/"
        )
        jac_files = [f for f in os.listdir(jac_directory) if f.endswith(".jac")]
        passed = 0
        for jac_file in jac_files:
            msg = "error in " + jac_file
            out = AstTool().print([jac_directory + jac_file])
            if out == "0:0 - 0:0\tModule\n0:0 - 0:0\t+-- EmptyToken - \n":
                continue
            self.assertIn("+-- Token", out, msg)
            self.assertIsNotNone(out, msg=msg)
            passed += 1
        self.assertGreater(passed, 10)

    def test_print_py(self) -> None:
        """Testing for print_py AstTool."""
        jac_py_directory = os.path.join(
            os.path.dirname(jaclang.__file__), "../examples/reference/"
        )
        jac_py_files = [
            f for f in os.listdir(jac_py_directory) if f.endswith((".jac", ".py"))
        ]
        for file in jac_py_files:
            msg = "error in " + file
            out = AstTool().print_py([jac_py_directory + file])
            if file.endswith(".jac"):
                self.assertIn("+-- ", out, msg)
                self.assertIsNotNone(out, msg=msg)
            elif file.endswith(".py"):
                if len(out.splitlines()) == 1:
                    continue
                self.assertIn("+-- ", out, msg)
                self.assertIsNotNone(out, msg=msg)

    def test_automated(self) -> None:
        """Testing for py, jac, md files for each content in Jac Grammer."""
        lark_path = os.path.join(os.path.dirname(jaclang.__file__), "compiler/jac.lark")
        headings_ = extract_headings(lark_path)
        snake_case_headings = [heading_to_snake(key) for key in headings_.keys()]
        refr_path = os.path.join(
            os.path.dirname(jaclang.__file__), "../examples/reference"
        )
        file_extensions = [".py", ".jac", ".md"]
        created_files = []
        for heading_name in snake_case_headings:
            for extension in file_extensions:
                file_name = heading_name + extension
                file_path = os.path.join(refr_path, file_name)
                self.assertTrue(
                    os.path.exists(file_path), f"File '{file_path}' does not exist."
                )
                created_files.append(file_path)
        all_reference_files = [
            os.path.join(refr_path, file)
            for file in os.listdir(refr_path)
            if os.path.isfile(os.path.join(refr_path, file))
        ]
        other_reference_files = [
            os.path.basename(file)
            for file in all_reference_files
            if file not in created_files
        ]
        self.assertEqual(len(other_reference_files), 0)
