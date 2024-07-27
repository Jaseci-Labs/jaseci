from jaclang.compiler.passes.ir_pass import Pass
from jaclang.compiler.passes.tool.fuse_comments_pass import (
    FuseCommentsPass as FuseCommentsPass,
)
from jaclang.compiler.passes.tool.jac_formatter_pass import (
    JacFormatPass as JacFormatPass,
)

__all__ = ["FuseCommentsPass", "JacFormatPass", "format_pass"]

format_pass: list[type[Pass]]
