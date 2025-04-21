"""Collection of passes for Jac IR."""

from typing import Type

from .sym_tab_build_pass import Pass, SymTabBuildPass  # noqa: I100
from .def_use_pass import DefUsePass  # noqa: I100
from .import_pass import JacImportPass, PyImportPass  # noqa: I100
from .def_impl_match_pass import DeclImplMatchPass  # noqa: I100
from .pyast_load_pass import PyastBuildPass  # type: ignore # noqa: I100
from .pyast_gen_pass import PyastGenPass  # noqa: I100
from .schedules import py_code_gen  # noqa: I100
from .type_check_pass import JacTypeCheckPass  # noqa: I100
from .registry_pass import RegistryPass  # noqa: I100
from .pybc_gen_pass import PyBytecodeGenPass  # noqa: I100
from .py_collect_dep_pass import PyCollectDepsPass  # noqa: I100
from .schedules import type_checker_sched  # noqa: I100


pass_schedule: list[Type[Pass]] = py_code_gen  # type: ignore[has-type]

__all__ = [
    "JacImportPass",
    "PyImportPass",
    "SymTabBuildPass",
    "DeclImplMatchPass",
    "DefUsePass",
    "PyastBuildPass",
    "PyastGenPass",
    "JacTypeCheckPass",
    "RegistryPass",
    "PyBytecodeGenPass",
    "type_checker_sched",
    "py_code_gen",
    "PyCollectDepsPass",
]
