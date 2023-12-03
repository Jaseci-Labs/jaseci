"""Pass schedules.

These are various pass schedules for the Jac compiler and static analysis.
"""
from __future__ import annotations


from .sub_node_tab_pass import SubNodeTabPass  # noqa: I100
from .import_pass import ImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .def_impl_match_pass import DeclDefMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .type_check_pass import JacTypeCheckPass  # noqa: I100

py_code_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    DefUsePass,
    PyastGenPass,
]

py_code_gen_typed = [
    *py_code_gen,
    JacTypeCheckPass,
]

py_compiler = [
    *py_code_gen,
    PyOutPass,
]
