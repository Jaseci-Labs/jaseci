"""Pass schedules."""

from typing import Type

from jaclang.compiler.passes.ir_pass import Pass
from jaclang.compiler.passes.tool.jac_formatter_pass import JacFormatPass  # noqa: I100


format_pass: list[Type[Pass]] = [JacFormatPass]

__all__ = [
    "JacFormatPass",
    "format_pass",
]
