"""Test pass module."""

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import DefUsePass
from jaclang.utils.test import TestCase


class DefUsePassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_def_uses(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(
            file_path=self.fixture_abs_path("defs_and_uses.jac"),
            target=DefUsePass,
        )
        # for i in state.unlinked:
        #     print(f"Unlinked {i.__class__.__name__} {i.sym_name} {i.loc}")
        # for i in state.linked:
        #     print(
        #         f"Linked {i.__class__.__name__} {i.sym_name} {i.loc} "
        #         f", {i.sym_link.decl.loc if i.sym_link else None}"
        #     )
        self.assertGreater(len(state.linked), 5)
        self.assertLess(len(state.warnings_had), 50)
        self.assertEqual(len(state.errors_had), 0)
