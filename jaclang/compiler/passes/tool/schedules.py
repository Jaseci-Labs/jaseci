"""Pass schedules."""

from typing import Type

from jaclang.compiler.passes.ir_pass import Pass
from jaclang.compiler.passes.tool.fuse_comments_pass import (
    FuseCommentsPass,
)  # noqa: I100
from jaclang.compiler.passes.tool.jac_formatter_pass import JacFormatPass  # noqa: I100


format_pass: list[Type[Pass]] = [FuseCommentsPass, JacFormatPass]

__all__ = [
    "FuseCommentsPass",
    "JacFormatPass",
    "format_pass",
]
