"""Pass schedules."""
from jaclang.jac.passes.main.sub_node_tab_pass import SubNodeTabPass
from jaclang.jac.passes.main.import_pass import ImportPass  # noqa: I100
from jaclang.jac.passes.main.sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from jaclang.jac.passes.main.def_impl_match_pass import DeclDefMatchPass  # noqa: I100
from jaclang.jac.passes.tool.ast_printer_pass import (  # noqa: I100
    AstDotGraphPass,
    AstPrinterPass,
)
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

__all__ = [
    "AstPrinterPass",
    "AstDotGraphPass",
    "SymbolTablePrinterPass",
    "SymbolTableDotGraphPass",
    "ast_dot_gen",
    "full_ast_dot_gen",
    "ast_print",
    "full_ast_print",
    "sym_tab_print",
    "sym_tab_dot_gen",
]
