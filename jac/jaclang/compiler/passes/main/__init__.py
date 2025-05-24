"""Collection of passes for Jac IR."""

from enum import Enum

from ..transform import Alert, Transform  # noqa: I100
from .annex_pass import JacAnnexPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass, UniPass  # noqa: I100
from .sym_tab_link_pass import SymTabLinkPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .import_pass import JacImportDepsPass, PyImportDepsPass  # noqa: I100
from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .pyast_load_pass import PyastBuildPass  # type: ignore # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .cfg_build_pass import CFGBuildPass  # noqa: I100
from .pyjac_ast_link_pass import PyJacAstLinkPass  # noqa: I100
from .inheritance_pass import InheritancePass  # noqa: I100
from .jtype_annotation_pass import JTypeAnnotatePass  # noqa: I100
from .jtype_check_pass import JTypeCheckPass  # noqa: I100
from .jtype_collect_pass import JTypeCollectPass  # noqa: I100


class CompilerMode(Enum):
    """Compiler modes."""

    PARSE = "PARSE"
    NO_CGEN = "NO_CGEN"
    NO_CGEN_SINGLE = "NO_CGEN_SINGLE"
    COMPILE = "COMPILE"
    COMPILE_SINGLE = "COMPILE_SINGLE"
    TYPECHECK = "TYPECHECK"
    QUICKCHECK = "QUICKCHECK"


__all__ = [
    "Alert",
    "Transform",
    "UniPass",
    "JacAnnexPass",
    "JacImportDepsPass",
    "PyImportDepsPass",
    "SymTabBuildPass",
    "SymTabLinkPass",
    "DeclImplMatchPass",
    "DefUsePass",
    "PyastBuildPass",
    "PyastGenPass",
    "PyBytecodeGenPass",
    "CompilerMode",
    "CFGBuildPass",
    "PyJacAstLinkPass",
    "InheritancePass",
    "JTypeAnnotatePass",
    "JTypeCheckPass",
    "JTypeCollectPass",
]
