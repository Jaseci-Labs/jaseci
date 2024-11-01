"""Test sub node pass module."""

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.utils.test import TestCase

# from jaclang.compiler.passes.main import SubNodeTabPass


class SubNodePassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_sub_node_pass(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            file_path=self.examples_abs_path("manual_code/circle.jac"),
        )
        for i in code_gen.ir.kid[1].kid:
            for k, v in i._sub_node_tab.items():
                for n in v:
                    self.assertIn(n, code_gen.get_all_sub_nodes(i, k, brute_force=True))
        self.assertFalse(code_gen.errors_had)
