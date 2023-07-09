"""Collection of passes for Jac IR."""

from .ir_pass import Pass
from .ast_build_pass import AstBuildPass  # noqa: I100
from .sub_node_tab_pass import SubNodeTabPass
from .import_pass import ImportPass  # noqa: I100
from .decl_def_match_pass import DeclDefMatchPass  # noqa: I100
from .type_analyze_pass import TypeAnalyzePass
from .blue_pygen_pass import BluePygenPass  # noqa: I100


__all__ = [
    "Pass",
    "AstBuildPass",
    "SubNodeTabPass",
    "ImportPass",
    "DeclDefMatchPass",
    "TypeAnalyzePass",
    "BluePygenPass",
]
