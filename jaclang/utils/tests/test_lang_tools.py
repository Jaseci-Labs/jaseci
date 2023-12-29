"""Test ast build pass module."""
import os

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

    def test_automated(self) -> None:
        """Testing for py, jac, md files for each content in Jac Grammer."""
        lark_path = os.path.join(os.getcwd(), "jaclang/compiler/jac.lark")
        headings_ = extract_headings(lark_path)
        snake_case_headings = [heading_to_snake(key) for key in headings_.keys()]
        refr_path = os.path.join(os.getcwd(), "examples/reference")
        file_extensions = [".py", ".jac", ".md"]
        for heading_name in snake_case_headings:
            for extension in file_extensions:
                file_name = heading_name + extension
                file_path = os.path.join(refr_path, file_name)
                self.assertTrue(
                    os.path.exists(file_path), f"File '{file_path}' does not exist."
                )
