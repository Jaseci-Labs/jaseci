"""Collection of passes for Jac IR."""

from .ast_build_pass import AstBuildPass
from .blue_pygen_pass import BluePygenPass
from .decl_def_match_pass import DeclDefMatchPass
from .import_pass import ImportPass
from .ir_pass import Pass
from .sub_node_tab_pass import SubNodeTabPass
from .type_analyze_pass import TypeAnalyzePass


__all__ = [
    "Pass",
    "AstBuildPass",
    "SubNodeTabPass",
    "ImportPass",
    "DeclDefMatchPass",
    "TypeAnalyzePass",
    "BluePygenPass",
]
