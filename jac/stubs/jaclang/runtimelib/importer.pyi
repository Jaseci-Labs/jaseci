import types
from _typeshed import Incomplete
from jaclang.compiler.absyntree import Module as Module
from jaclang.compiler.compile import compile_jac as compile_jac
from jaclang.runtimelib.machine import JacMachine as JacMachine
from jaclang.runtimelib.utils import sys_path_context as sys_path_context
from jaclang.utils.log import logging as logging

logger: Incomplete

class ImportPathSpec:
    target: Incomplete
    base_path: Incomplete
    absorb: Incomplete
    cachable: Incomplete
    mdl_alias: Incomplete
    override_name: Incomplete
    mod_bundle: Incomplete
    language: Incomplete
    items: Incomplete
    module_name: Incomplete
    package_path: Incomplete
    caller_dir: Incomplete
    full_target: Incomplete
    def __init__(
        self,
        target: str,
        base_path: str,
        absorb: bool,
        cachable: bool,
        mdl_alias: str | None,
        override_name: str | None,
        mod_bundle: Module | str | None,
        lng: str | None,
        items: dict[str, str | str | None] | None,
    ) -> None: ...
    def get_caller_dir(self) -> str: ...

class ImportReturn:
    ret_mod: Incomplete
    ret_items: Incomplete
    importer: Incomplete
    def __init__(
        self,
        ret_mod: types.ModuleType,
        ret_items: list[types.ModuleType],
        importer: Importer,
    ) -> None: ...
    def process_items(
        self,
        module: types.ModuleType,
        items: dict[str, str | str | None],
        caller_dir: str,
        lang: str | None,
        mod_bundle: Module | None = None,
        cachable: bool = True,
    ) -> None: ...
    def load_jac_mod_as_item(
        self,
        module: types.ModuleType,
        name: str,
        jac_file_path: str,
        mod_bundle: Module | None,
        cachable: bool,
        caller_dir: str,
    ) -> types.ModuleType | None: ...

class Importer:
    jac_machine: Incomplete
    result: Incomplete
    def __init__(self, jac_machine: JacMachine) -> None: ...
    def run_import(self, spec: ImportPathSpec) -> ImportReturn: ...
    def update_sys(self, module: types.ModuleType, spec: ImportPathSpec) -> None: ...
    def get_codeobj(
        self,
        full_target: str,
        module_name: str,
        mod_bundle: Module | None,
        cachable: bool,
        caller_dir: str,
    ) -> types.CodeType | None: ...

class PythonImporter(Importer):
    jac_machine: Incomplete
    def __init__(self, jac_machine: JacMachine) -> None: ...
    result: Incomplete
    def run_import(self, spec: ImportPathSpec) -> ImportReturn: ...

class JacImporter(Importer):
    jac_machine: Incomplete
    def __init__(self, jac_machine: JacMachine) -> None: ...
    def get_sys_mod_name(self, full_target: str) -> str: ...
    def handle_directory(
        self, module_name: str, full_mod_path: str, mod_bundle: Module | str | None
    ) -> types.ModuleType: ...
    def create_jac_py_module(
        self,
        mod_bundle: Module | str | None,
        module_name: str,
        package_path: str,
        full_target: str,
    ) -> types.ModuleType: ...
    result: Incomplete
    def run_import(self, spec: ImportPathSpec) -> ImportReturn: ...
