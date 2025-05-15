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
