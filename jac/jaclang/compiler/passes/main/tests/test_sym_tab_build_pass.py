"""Test pass module."""

# from jaclang.compiler.program import JacProgram
from jaclang.compiler.passes.main import SymTabBuildPass
from jaclang.utils.test import TestCase


class SymTabBuildPassTests(TestCase):
    """Test pass module."""

    TargetPass = SymTabBuildPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    # def test_name_collision(self) -> None:
    #     """Basic test for pass."""
    #     state = JacProgram().jac_file_to_pass(
    #         self.fixture_abs_path("multi_def_err.jac"), SymTabBuildPass
    #     )
    #     self.assertGreater(len(state.warnings_had), 0)
    #     self.assertIn("MyObject", str(state.warnings_had[0]))
