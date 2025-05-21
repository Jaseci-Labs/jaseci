"""Test ast build pass module."""

import ast as ast3
import os
from difflib import unified_diff

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes.tool import DocIRGenPass
from jaclang.compiler.program import JacProgram
from jaclang.utils.helpers import add_line_numbers
from jaclang.utils.test import AstSyncTestMixin, TestCase


class DocIrGenPassTests(TestCase, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = DocIRGenPass

    def test_corelib_fmt(self) -> None:
        """Parse micro jac file."""
        code_gen_format = JacProgram.jac_file_formatter(
            self.fixture_abs_path("corelib.jac"))
        print(code_gen_format)

    def test_circle_fmt(self) -> None:
        """Parse micro jac file."""
        code_gen_format = JacProgram.jac_file_formatter(
            self.examples_abs_path("manual_code/circle.jac"))
        print(code_gen_format)
