"""Living Workspace of Jac project."""

from __future__ import annotations

import os
from typing import Optional, Sequence

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.passes.main import DefUsePass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.passes.transform import Alert
from jaclang.compiler.symtable import Symbol, SymbolTable


def sym_tab_list(sym_tab: SymbolTable, file_path: str) -> Sequence[SymbolTable]:
    """Iterate through symbol table."""
    sym_tabs = (
        [sym_tab]
        if not (
            isinstance(sym_tab.owner, ast.Module)
            and sym_tab.owner.loc.mod_path != file_path
        )
        else []
    )
    for i in sym_tab.kid:
        sym_tabs += sym_tab_list(i, file_path=file_path)
    return sym_tabs


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: Optional[ast.Module],
        errors: Sequence[Alert],
        warnings: Sequence[Alert],
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.errors = errors
        self.warnings = warnings


class Workspace:
    """Class for managing workspace."""

    def __init__(self, path: str, lazy_parse: bool = False) -> None:
        """Initialize workspace."""
        self.path = path
        self.modules: dict[str, ModuleInfo] = {}
        self.lazy_parse = lazy_parse
        self.rebuild_workspace()

    def rebuild_workspace(self) -> None:
        """Rebuild workspace."""
        self.modules = {}
        for file in [
            os.path.normpath(os.path.join(root, name))
            for root, _, files in os.walk(self.path)
            for name in files
            if name.endswith(".jac")
        ]:
            if file in self.modules:
                continue
            if self.lazy_parse:
                # If lazy_parse is True, add the file to modules with empty IR
                self.modules[file] = ModuleInfo(
                    ir=None,
                    errors=[],
                    warnings=[],
                )
                continue

            with open(file, "r") as f:
                source = f.read()
            build = jac_str_to_pass(
                jac_str=source,
                file_path=file,
                target=DefUsePass,
            )
            if not isinstance(build.ir, ast.Module):
                src = ast.JacSource(source, mod_path=file)
                self.modules[file] = ModuleInfo(
                    ir=ast.Module(
                        name="",
                        doc=None,
                        body=[],
                        source=src,
                        is_imported=False,
                        kid=[src],
                    ),
                    errors=build.errors_had,
                    warnings=build.warnings_had,
                )
                continue
            self.modules[file] = ModuleInfo(
                ir=build.ir,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )
            if build.ir:
                for sub in build.ir.mod_deps:
                    self.modules[sub] = ModuleInfo(
                        ir=build.ir.mod_deps[sub],
                        errors=build.errors_had,
                        warnings=build.warnings_had,
                    )

    def rebuild_file(
        self, file_path: str, deep: bool = False, source: str = ""
    ) -> bool:
        """Rebuild a file."""
        if source == "":
            with open(file_path, "r") as f:
                source = f.read()
        build = jac_str_to_pass(
            jac_str=source,
            file_path=file_path,
            schedule=py_code_gen_typed,
        )
        if not isinstance(build.ir, ast.Module):
            src = ast.JacSource(source, mod_path=file_path)
            self.modules[file_path] = ModuleInfo(
                ir=ast.Module(
                    name="",
                    doc=None,
                    body=[],
                    source=src,
                    is_imported=False,
                    kid=[src],
                ),
                errors=build.errors_had,
                warnings=build.warnings_had,
            )
            return False
        self.modules[file_path] = ModuleInfo(
            ir=build.ir,
            errors=build.errors_had,
            warnings=build.warnings_had,
        )
        if deep:
            for sub in build.ir.mod_deps:
                self.modules[sub] = ModuleInfo(
                    ir=build.ir.mod_deps[sub],
                    errors=build.errors_had,
                    warnings=build.warnings_had,
                )
        return True

    def add_file(self, file_path: str) -> None:
        """Add a file to the workspace."""
        self.rebuild_file(file_path)

    def del_file(self, file_path: str) -> None:
        """Delete a file from the workspace."""
        del self.modules[file_path]

    def file_list(self) -> Sequence[str]:
        """Return a list of files in the workspace."""
        return list(self.modules.keys())

    def get_dependencies(
        self, file_path: str, deep: bool = False
    ) -> list[ast.ModulePath]:
        """Return a list of dependencies for a file."""
        mod_ir = self.modules[file_path].ir
        if deep:
            return (
                [
                    i
                    for i in mod_ir.get_all_sub_nodes(ast.ModulePath)
                    if i.parent_of_type(ast.Import).hint.tag.value == "jac"
                ]
                if mod_ir
                else []
            )
        else:
            return (
                [
                    i
                    for i in mod_ir.get_all_sub_nodes(ast.ModulePath)
                    if i.loc.mod_path == file_path
                    and i.parent_of_type(ast.Import).hint.tag.value == "jac"
                ]
                if mod_ir
                else []
            )

    def get_symbols(self, file_path: str) -> Sequence[Symbol]:
        """Return a list of symbols for a file."""
        symbols = []
        mod_ir = self.modules[file_path].ir
        if file_path in self.modules:
            root_table = mod_ir.sym_tab if mod_ir else None
            if file_path in self.modules and root_table:
                for i in sym_tab_list(sym_tab=root_table, file_path=file_path):
                    symbols += list(i.tab.values())
        return symbols

    def get_definitions(
        self, file_path: str
    ) -> Sequence[ast.AstSymbolNode]:  # need test
        """Return a list of definitions for a file."""
        defs = []
        for i in self.get_symbols(file_path):
            defs += i.defn
        return defs

    def get_uses(self, file_path: str) -> Sequence[ast.AstSymbolNode]:  # need test
        """Return a list of definitions for a file."""
        mod_ir = self.modules[file_path].ir
        uses: list[ast.AstSymbolNode] = []
        if self.lazy_parse:
            return uses
        if file_path in self.modules:
            root_table = mod_ir.sym_tab if mod_ir else None
            if file_path in self.modules and root_table:
                for i in sym_tab_list(sym_tab=root_table, file_path=file_path):
                    uses += i.uses
        return uses
