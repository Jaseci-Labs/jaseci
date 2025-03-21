"""Test registry pass."""

# import os

# from jaclang.compiler.compile import jac_file_to_pass
# from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
from jaclang.utils.test import TestCase


class RegistryPassTests(TestCase):
    """Test pass module."""

    # Need change
    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_registry_pass(self) -> None:
        """Basic test for pass."""
        # file_path = os.path.join(
        #     os.path.dirname(__file__),
        #     "fixtures",
        #     "symtab_link_tests",
        #     "main.jac",
        # )
        # print(file_path)
        # state = jac_file_to_pass(file_path, SymTabLinkPass)

        # self.assertIn("109", str(state.ir.to_dict()))
