"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

import re
from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import UniPass
from jaclang.compiler.unitree import UniNode
from jaclang.settings import settings


class JacFormatPass(UniPass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.comments: list[uni.CommentToken] = []
        self.indent_size = 4
        self.indent_level = 0
        self.MAX_LINE_LENGTH = settings.max_line_length

    def enter_module(self, node: uni.Module) -> None:
        self.comments = node.source.comments

    def exit_module(self, node: uni.Module) -> None:
        node.gen.jac = "# Formatted Jac Source Code"
