"""Living Workspace of Jac project."""

from __future__ import annotations

from typing import Optional, Sequence

from hashlib import md5

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.passes.transform import Alert
from jaclang.compiler.symtable import Symbol
from jaclang.langserve.utils import sym_tab_list, log, log_error
from jaclang.vendor.pygls.server import LanguageServer
from jaclang.vendor.pygls.workspace.text_document import TextDocument

import lsprotocol.types as lspt


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: ast.Module,
        errors: Sequence[Alert],
        warnings: Sequence[Alert],
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.errors = errors
        self.warnings = warnings
        self.diagnostics = self.gen_diagnostics()

    def gen_diagnostics(self) -> list[lspt.Diagnostic]:
        """Return diagnostics."""
        return [
            lspt.Diagnostic(
                range=lspt.Range(
                    start=lspt.Position(
                        line=error.loc.first_line, character=error.loc.col_start
                    ),
                    end=lspt.Position(
                        line=error.loc.last_line,
                        character=error.loc.col_end,
                    ),
                ),
                message=error.msg,
                severity=lspt.DiagnosticSeverity.Error,
            )
            for error in self.errors
        ] + [
            lspt.Diagnostic(
                range=lspt.Range(
                    start=lspt.Position(
                        line=warning.loc.first_line, character=warning.loc.col_start
                    ),
                    end=lspt.Position(
                        line=warning.loc.last_line,
                        character=warning.loc.col_end,
                    ),
                ),
                message=warning.msg,
                severity=lspt.DiagnosticSeverity.Warning,
            )
            for warning in self.warnings
        ]


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self):
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}

    def module_not_diff(self, doc: TextDocument) -> bool:
        """Check if module was changed."""
        return (
            doc.uri in self.modules
            and self.modules[doc.uri].ir.source.hash
            == md5(doc.source.encode()).hexdigest()
        )

    def quick_check(self, uri_path: str) -> None:
        """Rebuild a file."""
        document = self.workspace.get_document(uri_path)
        if self.module_not_diff(document):
            return
        try:
            build = jac_str_to_pass(
                jac_str=document.source,
                file_path=document.path,
                schedule=[],
            )
        except Exception as e:
            log_error(self, f"Error during syntax check: {e}")
        if isinstance(build.ir, ast.Module):
            self.modules[uri_path] = ModuleInfo(
                ir=build.ir,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )

    def push_diagnostics(self, uri_path: str) -> None:
        """Push diagnostics for a file."""
        if uri_path in self.modules:
            self.publish_diagnostics(
                uri_path,
                self.modules[uri_path].diagnostics,
            )

    def add_file(self, file_path: str) -> None:
        """Add a file to the workspace."""
        self.quick_check(file_path)

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

    def get_symbols(self, file_path: str) -> list[Symbol]:
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
