"""Test ast build pass module."""
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
