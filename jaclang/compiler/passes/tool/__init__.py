"""Collection of passes for Jac IR."""
from .ast_printer_pass import AstDotGraphPass, AstPrinterPass  # noqa: I100
from .sym_tab_printer_pass import (  # noqa: I100
    SymbolTableDotGraphPass,
    SymbolTablePrinterPass,
)
from .fuse_comments_pass import FuseCommentsPass  # noqa: I100
from .jac_formatter_pass import JacFormatPass  # noqa: I100

__all__ = [
    "AstDotGraphPass",
    "AstPrinterPass",
    "SymbolTablePrinterPass",
    "SymbolTableDotGraphPass",
    "FuseCommentsPass",
    "JacFormatPass",
]
