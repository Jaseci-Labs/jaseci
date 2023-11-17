"""Pass schedules."""
from typing import Type

from ..ir_pass import Pass

from jaclang.jac.passes.main.sub_node_tab_pass import SubNodeTabPass  # noqa: I100
from jaclang.jac.passes.main.import_pass import ImportPass  # noqa: I100
from jaclang.jac.passes.main.sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from jaclang.jac.passes.main.def_impl_match_pass import DeclDefMatchPass  # noqa: I100
from jaclang.jac.passes.tool.ast_printer_pass import (  # noqa: I100
    AstDotGraphPass,
    AstPrinterPass,
)
from jaclang.jac.passes.tool.fuse_comments_pass import FuseCommentsPass  # noqa: I100
from jaclang.jac.passes.tool.jac_formatter_pass import JacFormatPass  # noqa: I100
from jaclang.jac.passes.tool.sym_tab_printer_pass import (  # noqa: I100
    SymbolTableDotGraphPass,
    SymbolTablePrinterPass,
)

ast_dot_gen = [
    AstDotGraphPass,
]

full_ast_dot_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    AstDotGraphPass,
]

ast_print = [AstPrinterPass]

full_ast_print = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    AstPrinterPass,
]

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
    "AstPrinterPass",
    "AstDotGraphPass",
    "SymbolTablePrinterPass",
    "SymbolTableDotGraphPass",
    "FuseCommentsPass",
    "JacFormatPass",
    "ast_dot_gen",
    "full_ast_dot_gen",
    "ast_print",
    "full_ast_print",
    "sym_tab_print",
    "sym_tab_dot_gen",
    "format_pass",
]
