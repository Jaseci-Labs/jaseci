"""Living Workspace of Jac project."""
from __future__ import annotations

import os

import jaclang.jac.absyntree as ast
from jaclang.jac.passes.blue import DefUsePass
from jaclang.jac.passes.transform import Alert
from jaclang.jac.symtable import Symbol, SymbolTable
from jaclang.jac.transpiler import jac_str_to_pass


def sym_tab_list(sym_tab: SymbolTable, file_path: str) -> list[SymbolTable]:
    """Iterate through symbol table."""
    sym_tabs = (
        [sym_tab]
        if not (
            isinstance(sym_tab.owner, ast.Module)
            and sym_tab.owner.mod_path != file_path
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
        ir: ast.Module,
        errors: list[Alert],
        warnings: list[Alert],
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.errors = errors
        self.warnings = warnings


class Workspace:
    """Class for managing workspace."""

    def __init__(self, path: str) -> None:
        """Initialize workspace."""
        self.path = path
        self.modules: dict[str, ModuleInfo] = {}
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
            with open(file, "r") as f:
                source = f.read()
            build = jac_str_to_pass(
                jac_str=source,
                file_path=file,
                base_dir=self.path,
                target=DefUsePass,
            )
            if not isinstance(build.ir, ast.Module):
                self.modules[file] = ModuleInfo(
                    ir=ast.Module(
                        name="",
                        doc=None,
                        body=[],
                        source=ast.JacSource(source),
                        mod_path=file,
                        rel_mod_path="",
                        is_imported=False,
                        kid=[ast.EmptyToken()],
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
                for sub in build.ir.meta["sub_import_tab"]:
                    self.modules[sub] = ModuleInfo(
                        ir=build.ir.meta["sub_import_tab"][sub],
                        errors=build.errors_had,
                        warnings=build.warnings_had,
                    )

    def rebuild_file(self, file_path: str, deep: bool = False) -> bool:
        """Rebuild a file."""
        with open(file_path, "r") as f:
            source = f.read()
        build = jac_str_to_pass(
            jac_str=source,
            file_path=file_path,
            base_dir=self.path,
            target=DefUsePass,
        )
        if not isinstance(build.ir, ast.Module):
            self.modules[file_path] = ModuleInfo(
                ir=ast.Module(
                    name="",
                    doc=None,
                    body=[],
                    source=ast.JacSource(source),
                    mod_path=file_path,
                    rel_mod_path="",
                    is_imported=False,
                    kid=[ast.EmptyToken()],
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
            for sub in build.ir.meta["sub_import_tab"]:
                self.modules[sub] = ModuleInfo(
                    ir=build.ir.meta["sub_import_tab"][sub],
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

    def file_list(self) -> list[str]:
        """Return a list of files in the workspace."""
        return list(self.modules.keys())

    def get_dependencies(self, file_path: str, deep: bool = False) -> list[ast.Import]:
        """Return a list of dependencies for a file."""
        if deep:
            return self.modules[file_path].ir.get_all_sub_nodes(ast.Import)
        else:
            return [
                i
                for i in self.modules[file_path].ir.get_all_sub_nodes(ast.Import)
                if i.mod_link and i.mod_link.mod_path == file_path
            ]

    def get_symbols(self, file_path: str) -> list[Symbol]:
        """Return a list of symbols for a file."""
        symbols = []
        if file_path in self.modules:
            root_table = self.modules[file_path].ir.sym_tab
            if file_path in self.modules and isinstance(root_table, SymbolTable):
                for i in sym_tab_list(sym_tab=root_table, file_path=file_path):
                    symbols += list(i.tab.values())
        return symbols

    def get_definitions(self, file_path: str) -> list[ast.AstSymbolNode]:  # need test
        """Return a list of definitions for a file."""
        defs = []
        for i in self.get_symbols(file_path):
            defs += i.defn
        return defs

    def get_uses(self, file_path: str) -> list[ast.AstSymbolNode]:  # need test
        """Return a list of definitions for a file."""
        uses = []
        if file_path in self.modules:
            root_table = self.modules[file_path].ir.sym_tab
            if file_path in self.modules and isinstance(root_table, SymbolTable):
                for i in sym_tab_list(sym_tab=root_table, file_path=file_path):
                    uses += i.uses
        return uses
