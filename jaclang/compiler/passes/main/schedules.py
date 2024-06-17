"""Pass schedules.

These are various pass schedules for the Jac compiler and static analysis.
"""

from __future__ import annotations


from .sub_node_tab_pass import SubNodeTabPass  # noqa: I100
from .import_pass import JacImportPass, PyImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .pyjac_ast_link_pass import PyJacAstLinkPass  # noqa: I100
from .type_check_pass import JacTypeCheckPass  # noqa: I100
from .fuse_typeinfo_pass import FuseTypeInfoPass  # noqa: I100
from .registry_pass import RegistryPass  # noqa: I100
from .access_modifier_pass import AccessCheckPass  # noqa: I100

py_code_gen = [
    SubNodeTabPass,
    JacImportPass,
    PyImportPass,
    SymTabBuildPass,
    DeclImplMatchPass,
    DefUsePass,
    RegistryPass,
    PyastGenPass,
    PyJacAstLinkPass,
    PyBytecodeGenPass,
]

type_checker_sched = [JacTypeCheckPass, FuseTypeInfoPass, AccessCheckPass]
py_code_gen_typed = [*py_code_gen, *type_checker_sched]
py_compiler = [*py_code_gen, PyOutPass]
