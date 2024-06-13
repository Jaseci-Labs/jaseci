"""Living Workspace of Jac project."""

from __future__ import annotations

from enum import IntEnum
from hashlib import md5
from typing import Optional, Sequence


import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_ir_to_pass, jac_str_to_pass
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.schedules import type_checker_sched
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.passes.transform import Alert
from jaclang.langserve.utils import find_deepest_node_at_pos
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
        doc = self.workspace.get_text_document(uri)
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
        save_parent = (
            self.modules[file_path].parent if file_path in self.modules else None
        )
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
        self.modules[file_path].parent = save_parent
        for p in build.ir.mod_deps.keys():
            uri = uris.from_fs_path(p)
            self.modules[uri] = ModuleInfo(
                ir=build.ir.mod_deps[p],
                errors=[i for i in build.errors_had if i.loc.mod_path == p],
                warnings=[i for i in build.warnings_had if i.loc.mod_path == p],
                alev=alev,
            )
            self.modules[uri].parent = (
                self.modules[file_path] if file_path != uri else None
            )

    def quick_check(self, file_path: str, force: bool = False) -> None:
        """Rebuild a file."""
        if not force and self.module_not_diff(file_path, ALev.QUICK):
            return
        try:
            document = self.workspace.get_text_document(file_path)
            build = jac_str_to_pass(
                jac_str=document.source, file_path=document.path, schedule=[]
            )
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        self.update_modules(file_path, build, ALev.QUICK)

    def deep_check(self, file_path: str, force: bool = False) -> None:
        """Rebuild a file and its dependencies."""
        if file_path in self.modules:
            self.quick_check(file_path, force=force)
        if not force and self.module_not_diff(file_path, ALev.DEEP):
            return
        try:
            file_path = self.unwind_to_parent(file_path)
            build = jac_ir_to_pass(ir=self.modules[file_path].ir)
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
        self.update_modules(file_path, build, ALev.DEEP)

    def type_check(self, file_path: str, force: bool = False) -> None:
        """Rebuild a file and its dependencies."""
        if file_path not in self.modules:
            self.deep_check(file_path, force=force)
        if not force and self.module_not_diff(file_path, ALev.TYPE):
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
        document = self.workspace.get_text_document(file_path)
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
            document = self.workspace.get_text_document(file_path)
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

    def get_hover_info(
        self, file_path: str, position: lspt.Position
    ) -> Optional[lspt.Hover]:
        """Return hover information for a file."""
        node_selected = find_deepest_node_at_pos(
            self.modules[file_path].ir, position.line, position.character
        )
        value = self.get_node_info(node_selected) if node_selected else None
        if value:
            return lspt.Hover(
                contents=lspt.MarkupContent(
                    kind=lspt.MarkupKind.PlainText, value=f"{value}"
                ),
            )
        return None

    def get_node_info(self, node: ast.AstNode) -> Optional[str]:
        """Extract meaningful information from the AST node."""
        try:
            if isinstance(node, ast.Token):
                if isinstance(node, ast.AstSymbolNode):
                    if isinstance(node, ast.String):
                        return None
                    if node.sym_link and node.sym_link.decl:
                        decl_node = node.sym_link.decl
                        if isinstance(decl_node, ast.Architype):
                            if decl_node.doc:
                                node_info = f"({decl_node.arch_type.value}) {node.value} \n{decl_node.doc.lit_value}"
                            else:
                                node_info = (
                                    f"({decl_node.arch_type.value}) {node.value}"
                                )
                            if decl_node.semstr:
                                node_info += f"\n{decl_node.semstr.lit_value}"
                        elif isinstance(decl_node, ast.Ability):
                            node_info = f"(ability) can {node.value}"
                            if decl_node.signature:
                                node_info += f" {decl_node.signature.unparse()}"
                            if decl_node.doc:
                                node_info += f"\n{decl_node.doc.lit_value}"
                            if decl_node.semstr:
                                node_info += f"\n{decl_node.semstr.lit_value}"
                        elif isinstance(decl_node, ast.Name):
                            if (
                                decl_node.parent
                                and isinstance(decl_node.parent, ast.SubNodeList)
                                and decl_node.parent.parent
                                and isinstance(decl_node.parent.parent, ast.Assignment)
                                and decl_node.parent.parent.type_tag
                            ):
                                node_info = (
                                    f"(variable) {decl_node.value}: "
                                    f"{decl_node.parent.parent.type_tag.unparse()}"
                                )
                                if decl_node.parent.parent.semstr:
                                    node_info += (
                                        f"\n{decl_node.parent.parent.semstr.lit_value}"
                                    )
                            else:
                                if decl_node.value in [
                                    "str",
                                    "int",
                                    "float",
                                    "bool",
                                    "bytes",
                                    "list",
                                    "tuple",
                                    "set",
                                    "dict",
                                    "type",
                                ]:
                                    node_info = f"({decl_node.value}) Built-in type"
                                else:
                                    node_info = f"(variable) {decl_node.value}: None"
                        elif isinstance(decl_node, ast.HasVar):
                            if decl_node.type_tag:
                                node_info = f"(variable) {decl_node.name.value} {decl_node.type_tag.unparse()}"
                            else:
                                node_info = f"(variable) {decl_node.name.value}"
                            if decl_node.semstr:
                                node_info += f"\n{decl_node.semstr.lit_value}"
                        elif isinstance(decl_node, ast.ParamVar):
                            if decl_node.type_tag:
                                node_info = f"(parameter) {decl_node.name.value} {decl_node.type_tag.unparse()}"
                            else:
                                node_info = f"(parameter) {decl_node.name.value}"
                            if decl_node.semstr:
                                node_info += f"\n{decl_node.semstr.lit_value}"
                        elif isinstance(decl_node, ast.ModuleItem):
                            node_info = (
                                f"(ModuleItem) {node.value}"  # TODO: Add more info
                            )
                        else:
                            node_info = f"{node.value}"
                    else:
                        node_info = f"{node.value}"  # non symbol node
                else:
                    return None
            else:
                return None
        except AttributeError as e:
            self.log_warning(f"Attribute error when accessing node attributes: {e}")
        return node_info.strip()

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
