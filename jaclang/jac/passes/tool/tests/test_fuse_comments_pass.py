"""Test ast build pass module."""
import ast as ast3


from jaclang.jac.passes.main import PyastGenPass
from jaclang.jac.passes.main.schedules import py_code_gen as without_format
from jaclang.jac.passes.tool import JacFormatPass
from jaclang.jac.transpiler import jac_file_to_pass, jac_str_to_pass
from jaclang.utils.test import TestCase


class FuseCommentsPassTests:
    """Test pass module."""

    TargetPass = JacFormatPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_simple(self) -> None:
        """Basic test for pass."""
        code1 = f"with entry #* hi *# {{print('hi');}}"
