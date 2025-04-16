"""Pass schedules.

These are various pass schedules for the Jac compiler and static analysis.
"""

from __future__ import annotations

from typing import Type

from jaclang.compiler.passes import Pass

from .import_pass import PyImportPass  # noqa: I100
from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .pyjac_ast_link_pass import PyJacAstLinkPass  # noqa: I100
from .fuse_typeinfo_pass import FuseTypeInfoPass  # noqa: I100
from .registry_pass import RegistryPass  # noqa: I100
from .access_modifier_pass import AccessCheckPass  # noqa: I100
from .py_collect_dep_pass import PyCollectDepsPass  # noqa: I100
from .inheritance_pass import InheritancePass  # noqa: I100

py_code_gen: list[Type[Pass]] = [
    DeclImplMatchPass,
    DefUsePass,
    RegistryPass,
    PyastGenPass,
    PyJacAstLinkPass,
    PyBytecodeGenPass,
]

type_checker_sched: list[Type[Pass]] = [
    PyCollectDepsPass,
    PyImportPass,
    DefUsePass,
    InheritancePass,
    FuseTypeInfoPass,
    AccessCheckPass,
]
py_code_gen_typed = [*py_code_gen, *type_checker_sched]
# py_code_gen_build should be like py_code_gen_typed but without the PyImportPass
py_code_gen_build = [i for i in py_code_gen if i != PyImportPass]
