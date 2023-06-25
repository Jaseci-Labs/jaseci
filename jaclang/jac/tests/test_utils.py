"""Tests for Jac utils."""
from jaclang.jac.utils import load_ast_and_print_pass_template
from jaclang.utils.test import TestCase


class TestLexer(TestCase):
    """Test Jac utils."""

    def test_ast_template_loader(self) -> None:
        """Basic test for ast template loader."""
        output = load_ast_and_print_pass_template()
        self.assertGreater(len(output), 1000)
