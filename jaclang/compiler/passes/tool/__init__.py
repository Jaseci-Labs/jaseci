"""Collection of passes for Jac IR."""
from .ast_printer_pass import AstDotGraphPass, AstPrinterPass  # noqa: I100
from .sym_tab_printer_pass import (  # noqa: I100
    SymbolTableDotGraphPass,
    SymbolTablePrinterPass,
)
from .jac_formatter_pass import JacFormatPass  # noqa: I100

__all__ = [
    "AstDotGraphPass",
    "AstPrinterPass",
    "SymbolTablePrinterPass",
    "SymbolTableDotGraphPass",
    "JacFormatPass",
]
