"""Pass schedules."""
from typing import Type

from jaclang.compiler.passes.ir_pass import Pass
from jaclang.compiler.passes.main.def_impl_match_pass import (
    DeclDefMatchPass,
)  # noqa: I100
from jaclang.compiler.passes.main.sub_node_tab_pass import SubNodeTabPass  # noqa: I100
from jaclang.compiler.passes.main.import_pass import ImportPass  # noqa: I100
from jaclang.compiler.passes.main.sym_tab_build_pass import (
    SymTabBuildPass,
)  # noqa: I100
from jaclang.compiler.passes.tool.fuse_comments_pass import (
    FuseCommentsPass,
)  # noqa: I100
from jaclang.compiler.passes.tool.jac_formatter_pass import JacFormatPass  # noqa: I100
from jaclang.compiler.passes.tool.sym_tab_printer_pass import (  # noqa: I100
    SymbolTableDotGraphPass,
    SymbolTablePrinterPass,
)

sym_tab_print = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    SymbolTablePrinterPass,
]

sym_tab_dot_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    SymbolTableDotGraphPass,
]

format_pass: list[Type[Pass]] = [FuseCommentsPass, JacFormatPass]

__all__ = [
    "SymbolTablePrinterPass",
    "SymbolTableDotGraphPass",
    "FuseCommentsPass",
    "JacFormatPass",
    "sym_tab_print",
    "sym_tab_dot_gen",
    "format_pass",
]
