"""Living Workspace of Jac project."""

from __future__ import annotations

from hashlib import md5
from typing import Sequence, Type


import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_pass_to_pass, jac_str_to_pass
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.schedules import (
    AccessCheckPass,
    PyBytecodeGenPass,
    py_code_gen_typed,
)
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.passes.transform import Alert
from jaclang.compiler.symtable import Symbol
from jaclang.langserve.utils import sym_tab_list
from jaclang.vendor.pygls.server import LanguageServer
from jaclang.vendor.pygls.workspace.text_document import TextDocument

import lsprotocol.types as lspt


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: ast.Module,
        to_pass: Pass,
        errors: Sequence[Alert],
        warnings: Sequence[Alert],
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.at_pass = to_pass
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

    def __init__(self) -> None:
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

    def module_reached_pass(self, doc: TextDocument, target: Type[Pass]) -> bool:
        """Check if module reached a pass."""
        return doc.uri in self.modules and isinstance(
            self.modules[doc.uri].at_pass, target
        )

    def push_diagnostics(self, file_path: str) -> None:
        """Push diagnostics for a file."""
        if file_path in self.modules:
            self.publish_diagnostics(
                file_path,
                self.modules[file_path].diagnostics,
            )

    def quick_check(self, file_path: str) -> None:
        """Rebuild a file."""
        document = self.workspace.get_document(file_path)
        if self.module_not_diff(document):
            return
        try:
            build = jac_str_to_pass(
                jac_str=document.source, file_path=document.path, schedule=[]
            )
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        if isinstance(build.ir, ast.Module):
            self.modules[file_path] = ModuleInfo(
                ir=build.ir,
                to_pass=build,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )

    def deep_check(self, file_path: str) -> None:
        """Rebuild a file and its dependencies."""
        document = self.workspace.get_document(file_path)
        if self.module_not_diff(document) and self.module_reached_pass(
            document, PyBytecodeGenPass
        ):
            return
        try:
            build = jac_pass_to_pass(in_pass=self.modules[file_path].at_pass)
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        if isinstance(build.ir, ast.Module):
            self.modules[file_path] = ModuleInfo(
                ir=build.ir,
                to_pass=build,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )

    def type_check(self, file_path: str) -> None:
        """Rebuild a file and its dependencies."""
        document = self.workspace.get_document(file_path)
        if self.module_not_diff(document) and self.module_reached_pass(
            document, AccessCheckPass
        ):
            return
        try:
            build = jac_pass_to_pass(
                in_pass=self.modules[file_path].at_pass,
                target=AccessCheckPass,
                schedule=py_code_gen_typed,
            )
        except Exception as e:
            self.log_error(f"Error during type check: {e}")
        if isinstance(build.ir, ast.Module):
            self.modules[file_path] = ModuleInfo(
                ir=build.ir,
                to_pass=build,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )

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
