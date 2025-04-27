"""Pass schedules.

These are various pass schedules for the Jac compiler and static analysis.
"""

from __future__ import annotations

from enum import Enum

from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .pyjac_ast_link_pass import PyJacAstLinkPass  # noqa: I100
from .fuse_typeinfo_pass import FuseTypeInfoPass  # noqa: I100
from .registry_pass import RegistryPass  # noqa: I100
from .access_modifier_pass import AccessCheckPass  # noqa: I100
from .inheritance_pass import InheritancePass  # noqa: I100


class CompilerMode(Enum):
    """Compiler modes."""

    PARSE = "PARSE"
    COMPILE = "COMPILE"
    TYPECHECK = "TYPECHECK"


py_code_gen = [
    DeclImplMatchPass,
    DefUsePass,
    RegistryPass,
    PyastGenPass,
    PyJacAstLinkPass,
    PyBytecodeGenPass,
]

type_checker_sched = [
    InheritancePass,
    FuseTypeInfoPass,
    AccessCheckPass,
]

py_code_gen_typed = [*py_code_gen, *type_checker_sched]
