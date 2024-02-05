"""Collection of passes for Jac IR."""

from .def_impl_match_pass import DeclDefMatchPass
from .def_use_pass import DefUsePass
from .import_pass import ImportPass
from .pyast_gen_pass import PyastGenPass
from .pyast_load_pass import PyastBuildPass  # type: ignore
from .pyout_pass import PyOutPass
from .schedules import py_code_gen
from .sub_node_tab_pass import SubNodeTabPass
from .sym_tab_build_pass import SymTabBuildPass
from .type_check_pass import JacTypeCheckPass


pass_schedule = py_code_gen

__all__ = [
    "SubNodeTabPass",
    "ImportPass",
    "SymTabBuildPass",
    "DeclDefMatchPass",
    "DefUsePass",
    "PyOutPass",
    "PyastBuildPass",
    "PyastGenPass",
    "JacTypeCheckPass",
]
