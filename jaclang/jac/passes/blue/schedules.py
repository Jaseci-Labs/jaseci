"""Pass schedules."""
from .sub_node_tab_pass import SubNodeTabPass  # noqa: I100
from .import_pass import ImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .def_impl_match_pass import DeclDefMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .blue_pygen_pass import BluePygenPass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .jac_formatter_pass import JacFormatPass  # noqa: I100

py_code_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    DefUsePass,
    BluePygenPass,
]

py_transpiler = [
    *py_code_gen,
    PyOutPass,
]

format_pass = [JacFormatPass]
