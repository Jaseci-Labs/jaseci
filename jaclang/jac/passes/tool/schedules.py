"""Pass schedules."""
from jaclang.jac.passes.blue.sub_node_tab_pass import SubNodeTabPass
from jaclang.jac.passes.blue.import_pass import ImportPass  # noqa: I100
from jaclang.jac.passes.blue.sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from jaclang.jac.passes.blue.decl_def_match_pass import DeclDefMatchPass  # noqa: I100
from jaclang.jac.passes.tool.dot_exporter_pass import DotGraphPass  # noqa: I100
from jaclang.jac.passes.tool.ast_printer_pass import ASTPrinterPass  # noqa: I100
from jaclang.jac.passes.tool.sym_tab_printer_pass import (  # noqa: I100
    SymbolTablePrinterPass,
)
from jaclang.jac.passes.tool.sym_tab_dot_exporter_pass import (  # noqa: I100
    SymtabDotGraphPass,
)

ast_dot_gen = [
    DotGraphPass,
]

full_ast_dot_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    DotGraphPass,
]

ast_print = [ASTPrinterPass]

full_ast_print = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    ASTPrinterPass,
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
    SymtabDotGraphPass,
]
