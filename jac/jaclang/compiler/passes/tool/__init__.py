"""Collection of passes for Jac IR."""

from .fuse_comments_pass import FuseCommentsPass  # noqa: I100
from .jac_formatter_pass import JacFormatPass  # noqa: I100
from .new_formatter_pass import NewJacFormatPass  # noqa: I100

__all__ = [
    "FuseCommentsPass",
    "JacFormatPass",
    "NewJacFormatPass",
]
