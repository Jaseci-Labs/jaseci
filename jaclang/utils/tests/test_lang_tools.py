"""Test ast build pass module."""
import os

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
        current_directory = os.getcwd()
        jac_directory = current_directory + "/examples/reference/"
        jac_files = [f for f in os.listdir(jac_directory) if f.endswith(".jac")]
        exclude = ["match_litteral_patterns.jac", "ignore_statements"]
        for jac_file in jac_files:
            if jac_file in exclude:
                continue
            if jac_file.endswith(".jac"):
                # # Check the forbidden strings in the output of AstTool().print
                msg = "error in " + jac_file
                out = AstTool().print([jac_directory + jac_file])
                self.assertIn("+-- Token", out, msg)
                self.assertIsNotNone(out, msg=msg)
