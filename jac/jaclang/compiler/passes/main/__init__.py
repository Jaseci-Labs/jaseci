"""Collection of passes for Jac IR."""

from .annex_pass import JacAnnexManager  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass, UniPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .import_pass import JacImportPass, PyImportPass  # noqa: I100
from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .pyast_load_pass import PyastBuildPass  # type: ignore # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .schedules import py_code_gen  # noqa: I100
from .type_check_pass import JacTypeCheckPass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .py_collect_dep_pass import PyCollectDepsPass  # noqa: I100
from .schedules import CompilerMode, analysis_sched, type_checker_sched  # noqa: I100

__all__ = [
    "UniPass",
    "JacAnnexManager",
    "JacImportPass",
    "PyImportPass",
    "SymTabBuildPass",
    "DeclImplMatchPass",
    "DefUsePass",
    "PyastBuildPass",
    "PyastGenPass",
    "JacTypeCheckPass",
    "PyBytecodeGenPass",
    "CompilerMode",
    "type_checker_sched",
    "py_code_gen",
    "analysis_sched",
    "PyCollectDepsPass",
]
