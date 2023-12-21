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
        """Testing for "<", ">", and ">>" in the dot file generation."""
        """run in Main Jaclang directory."""
        current_directory = os.getcwd()
        dummy_dotout = os.path.join(os.path.dirname(__file__), "dummy_output.dot")
        l: int = 0
        for root, _, files in os.walk(current_directory):
            for jac_file in files:
                if jac_file.endswith(".jac"):
                    l += 1
                    jac_file_path = os.path.join(root, jac_file)
                    dummy_args = [jac_file_path, dummy_dotout]
                    AstTool().gen_dotfile(dummy_args)
                    with open(dummy_dotout, "r") as file:
                        file_content = file.read()
                        forbidden_strings = ["<<", ">>", "<init>", "<super>"]
                        if any(
                            forbidden_string in file_content
                            for forbidden_string in forbidden_strings
                        ):
                            raise AssertionError(f"Assertion failed in file {jac_file}")
                        else:
                            print(l, jac_file, " PASSED")
