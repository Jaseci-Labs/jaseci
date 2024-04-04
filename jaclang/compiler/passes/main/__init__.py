"""Collection of passes for Jac IR."""

from .sub_node_tab_pass import SubNodeTabPass
from .import_pass import ImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .def_impl_match_pass import DeclDefMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .pyast_load_pass import PyastBuildPass  # type: ignore # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .schedules import py_code_gen  # noqa: I100
from .type_check_pass import JacTypeCheckPass  # noqa: I100
from .registry_pass import RegistryPass  # noqa: I100


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
    "RegistryPass",
]
