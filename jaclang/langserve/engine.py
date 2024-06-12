"""Living Workspace of Jac project."""

from __future__ import annotations

from enum import IntEnum
from hashlib import md5
from typing import Any, Generator, Optional, Sequence


import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_ir_to_pass, jac_str_to_pass
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.schedules import type_checker_sched
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.passes.transform import Alert
from jaclang.compiler.symtable import Symbol
from jaclang.langserve.utils import position_within_node, sym_tab_list
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


class ALev(IntEnum):
    """Analysis Level."""

    QUICK = 1
    DEEP = 2
    TYPE = 3


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: ast.Module,
        errors: Sequence[Alert],
        warnings: Sequence[Alert],
        alev: ALev,
        parent: Optional[ModuleInfo] = None,
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.errors = errors
        self.warnings = warnings
        self.alev = alev
        self.parent: Optional[ModuleInfo] = parent
        self.diagnostics = self.gen_diagnostics()

    @property
    def uri(self) -> str:
        """Return uri."""
        return uris.from_fs_path(self.ir.loc.mod_path)

    @property
    def has_syntax_error(self) -> bool:
        """Return if there are syntax errors."""
        return len(self.errors) > 0 and self.alev == ALev.QUICK

    def gen_diagnostics(self) -> list[lspt.Diagnostic]:
        """Return diagnostics."""
        return [
            lspt.Diagnostic(
                range=lspt.Range(
                    start=lspt.Position(
                        line=error.loc.first_line - 1, character=error.loc.col_start - 1
                    ),
                    end=lspt.Position(
                        line=error.loc.last_line - 1,
                        character=error.loc.col_end - 1,
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
                        line=warning.loc.first_line - 1,
                        character=warning.loc.col_start - 1,
                    ),
                    end=lspt.Position(
                        line=warning.loc.last_line - 1,
                        character=warning.loc.col_end - 1,
                    ),
                ),
                message=warning.msg,
                severity=lspt.DiagnosticSeverity.Warning,
            )
            for warning in self.warnings
        ]


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self) -> None:
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}

    def module_not_diff(self, uri: str, alev: ALev) -> bool:
        """Check if module was changed."""
        doc = self.workspace.get_document(uri)
        return (
            doc.uri in self.modules
            and self.modules[doc.uri].ir.source.hash
            == md5(doc.source.encode()).hexdigest()
            and (
                self.modules[doc.uri].alev >= alev
                or self.modules[doc.uri].has_syntax_error
            )
        )

    def push_diagnostics(self, file_path: str) -> None:
        """Push diagnostics for a file."""
        if file_path in self.modules:
            self.publish_diagnostics(
                file_path,
                self.modules[file_path].diagnostics,
            )

    def unwind_to_parent(self, file_path: str) -> str:
        """Unwind to parent."""
        if file_path in self.modules:
            while cur := self.modules[file_path].parent:
                file_path = cur.uri
        return file_path

    def update_modules(self, file_path: str, build: Pass, alev: ALev) -> None:
        """Update modules."""
        if not isinstance(build.ir, ast.Module):
            self.log_error("Error with module build.")
            return
        self.modules[file_path] = ModuleInfo(
            ir=build.ir,
            errors=[
                i
                for i in build.errors_had
                if i.loc.mod_path == uris.to_fs_path(file_path)
            ],
            warnings=[
                i
                for i in build.warnings_had
                if i.loc.mod_path == uris.to_fs_path(file_path)
            ],
            alev=alev,
        )
        for p in build.ir.mod_deps.keys():
            uri = uris.from_fs_path(p)
            self.modules[uri] = ModuleInfo(
                ir=build.ir.mod_deps[p],
                errors=[i for i in build.errors_had if i.loc.mod_path == p],
                warnings=[i for i in build.warnings_had if i.loc.mod_path == p],
                alev=alev,
            )

    def quick_check(self, file_path: str) -> None:
        """Rebuild a file."""
        if self.module_not_diff(file_path, ALev.QUICK):
            return
        try:
            document = self.workspace.get_document(file_path)
            build = jac_str_to_pass(
                jac_str=document.source, file_path=document.path, schedule=[]
            )
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        self.update_modules(file_path, build, ALev.QUICK)

    def deep_check(self, file_path: str) -> None:
        """Rebuild a file and its dependencies."""
        if file_path in self.modules:
            self.quick_check(file_path)
        if self.module_not_diff(file_path, ALev.DEEP):
            return
        try:
            file_path = self.unwind_to_parent(file_path)
            build = jac_ir_to_pass(ir=self.modules[file_path].ir)
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        self.update_modules(file_path, build, ALev.DEEP)

    def type_check(self, file_path: str) -> None:
        """Rebuild a file and its dependencies."""
        if file_path not in self.modules:
            self.deep_check(file_path)
        if self.module_not_diff(file_path, ALev.TYPE):
            return
        try:
            file_path = self.unwind_to_parent(file_path)
            build = jac_ir_to_pass(
                ir=self.modules[file_path].ir, schedule=type_checker_sched
            )
        except Exception as e:
            self.log_error(f"Error during type check: {e}")
        self.update_modules(file_path, build, ALev.TYPE)

    def get_completion(
        self, file_path: str, position: lspt.Position
    ) -> lspt.CompletionList:
        """Return completion for a file."""
        items = []
        document = self.workspace.get_document(file_path)
        current_line = document.lines[position.line].strip()
        if current_line.endswith("hello."):

            items = [
                lspt.CompletionItem(label="world"),
                lspt.CompletionItem(label="friend"),
            ]
        return lspt.CompletionList(is_incomplete=False, items=items)

    def rename_module(self, old_path: str, new_path: str) -> None:
        """Rename module."""
        if old_path in self.modules and new_path != old_path:
            self.modules[new_path] = self.modules[old_path]
            del self.modules[old_path]

    def delete_module(self, uri: str) -> None:
        """Delete module."""
        if uri in self.modules:
            del self.modules[uri]

    def formatted_jac(self, file_path: str) -> list[lspt.TextEdit]:
        """Return formatted jac."""
        try:
            document = self.workspace.get_document(file_path)
            format = jac_str_to_pass(
                jac_str=document.source,
                file_path=document.path,
                target=JacFormatPass,
                schedule=[FuseCommentsPass, JacFormatPass],
            )
            formatted_text = (
                format.ir.gen.jac
                if JacParser not in [e.from_pass for e in format.errors_had]
                else document.source
            )
        except Exception as e:
            self.log_error(f"Error during formatting: {e}")
            formatted_text = document.source
        return [
            lspt.TextEdit(
                range=lspt.Range(
                    start=lspt.Position(line=0, character=0),
                    end=lspt.Position(
                        line=len(document.source.splitlines()) + 1, character=0
                    ),
                ),
                new_text=(formatted_text),
            )
        ]

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

    def find_deepest_node(
        self, node: ast.AstNode, line: int, character: int
    ) -> Generator[Any, Any, Any]:
        """Find the deepest node that contains the given position."""
        if position_within_node(node, line, character):
            yield node
            for child in node.kid:
                yield from self.find_deepest_node(child, line, character)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        self.show_message_log(message, lspt.MessageType.Error)
        self.show_message(message, lspt.MessageType.Error)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.show_message_log(message, lspt.MessageType.Warning)
        self.show_message(message, lspt.MessageType.Warning)

    def log_info(self, message: str) -> None:
        """Log an info message."""
        self.show_message_log(message, lspt.MessageType.Info)
        self.show_message(message, lspt.MessageType.Info)
