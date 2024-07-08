"""Living Workspace of Jac project."""

from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from enum import IntEnum
from typing import Optional


import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_ir_to_pass, jac_str_to_pass
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.schedules import type_checker_sched
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.passes.transform import Alert
from jaclang.langserve.utils import (
    collect_symbols,
    create_range,
    find_deepest_symbol_node_at_pos,
    get_item_path,
    get_mod_path,
)
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


class ALev(IntEnum):
    """Analysis Level successfully completed."""

    QUICK = 1
    DEEP = 2
    TYPE = 3


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: ast.Module,
        errors: list[Alert],
        warnings: list[Alert],
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
        self.sem_tokens: list[int] = self.gen_sem_tokens()

    @property
    def uri(self) -> str:
        """Return uri."""
        return uris.from_fs_path(self.ir.loc.mod_path)

    def update_with(
        self,
        build: Pass,
        alev: ALev,
        refresh: bool = False,
        mod_override: Optional[ast.Module] = None,
    ) -> None:
        """Update module info."""
        target_mod = mod_override if mod_override else build.ir
        if not isinstance(target_mod, ast.Module):
            return
        self.ir = target_mod  # if alev > ALev.QUICK else self.ir
        if refresh:
            self.errors = build.errors_had
            self.warnings = build.warnings_had
        else:
            self.errors += [
                i
                for i in build.errors_had
                if i not in self.errors
                if i.loc.mod_path == target_mod.loc.mod_path
            ]
            self.warnings += [
                i
                for i in build.warnings_had
                if i not in self.warnings
                if i.loc.mod_path == target_mod.loc.mod_path
            ]
        self.alev = alev
        self.diagnostics = self.gen_diagnostics()
        if self.alev == ALev.TYPE:
            self.sem_tokens = self.gen_sem_tokens()

    def gen_diagnostics(self) -> list[lspt.Diagnostic]:
        """Return diagnostics."""
        return [
            lspt.Diagnostic(
                range=create_range(error.loc),
                message=error.msg,
                severity=lspt.DiagnosticSeverity.Error,
            )
            for error in self.errors
        ] + [
            lspt.Diagnostic(
                range=create_range(warning.loc),
                message=warning.msg,
                severity=lspt.DiagnosticSeverity.Warning,
            )
            for warning in self.warnings
        ]

    def gen_sem_tokens(self) -> list[int]:
        """Return semantic tokens."""
        tokens = []
        prev_line, prev_col = 0, 0
        for node in self.ir._in_mod_nodes:
            if isinstance(node, ast.NameAtom) and node.sem_token:
                line, col_start, col_end = (
                    node.loc.first_line - 1,
                    node.loc.col_start - 1,
                    node.loc.col_end - 1,
                )
                length = col_end - col_start
                tokens += [
                    line - prev_line,
                    col_start if line != prev_line else col_start - prev_col,
                    length,
                    *node.sem_token,
                ]
                prev_line, prev_col = line, col_start
        return tokens

    def update_sem_tokens(
        self, content_changes: lspt.DidChangeTextDocumentParams
    ) -> list[int]:
        """Update semantic tokens on change."""
        for change in [
            x
            for x in content_changes.content_changes
            if isinstance(x, lspt.TextDocumentContentChangeEvent_Type1)
        ]:
            logging.info(f"Change: {change}")
            start_line = change.range.start.line
            start_character = change.range.start.character
            end_line = change.range.end.line
            end_character = change.range.end.character

            # Calculate the change in number of lines and characters
            line_delta = change.text.count("\n") - (end_line - start_line)
            if line_delta == 0:
                char_delta = len(change.text) - (end_character - start_character)
            else:
                last_newline_index = change.text.rfind("\n")
                char_delta = (
                    len(change.text)
                    - last_newline_index
                    - 1
                    - end_character
                    + start_character
                )

            # Update the token list
            i = 0
            while i < len(self.sem_tokens):
                token_line = self.sem_tokens[i]
                token_start_char = self.sem_tokens[i + 1]

                if token_line > start_line or (
                    token_line == start_line and token_start_char >= start_character
                ):
                    self.sem_tokens[i] += line_delta
                    if token_line == start_line:
                        self.sem_tokens[i + 1] += char_delta

                i += 5

        return self.sem_tokens


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self) -> None:
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}
        self.executor = ThreadPoolExecutor()

    async def push_diagnostics(self, file_path: str) -> None:
        """Push diagnostics for a file."""
        if file_path in self.modules:
            self.publish_diagnostics(
                file_path,
                self.modules[file_path].diagnostics,
            )

    def unwind_to_parent(self, file_path: str) -> str:
        """Unwind to parent."""
        orig_file_path = file_path
        if file_path in self.modules:
            while cur := self.modules[file_path].parent:
                file_path = cur.uri
            if file_path == orig_file_path and (
                discover := self.modules[file_path].ir.annexable_by
            ):
                file_path = uris.from_fs_path(discover)
                self.quick_check(file_path)
        return file_path

    def update_modules(
        self, file_path: str, build: Pass, alev: ALev, refresh: bool = False
    ) -> None:
        """Update modules."""
        if not isinstance(build.ir, ast.Module):
            self.log_error("Error with module build.")
            return
        if file_path in self.modules:
            self.modules[file_path].update_with(build, alev, refresh=refresh)
        else:
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
            if not refresh and uri in self.modules:
                self.modules[uri].update_with(
                    build, alev, mod_override=build.ir.mod_deps[p], refresh=refresh
                )
            else:
                self.modules[uri] = ModuleInfo(
                    ir=build.ir.mod_deps[p],
                    errors=[i for i in build.errors_had if i.loc.mod_path == p],
                    warnings=[i for i in build.warnings_had if i.loc.mod_path == p],
                    alev=alev,
                )
            self.modules[uri].parent = (
                self.modules[file_path] if file_path != uri else None
            )

    def quick_check(self, file_path: str) -> bool:
        """Rebuild a file."""
        try:
            document = self.workspace.get_text_document(file_path)
            build = jac_str_to_pass(
                jac_str=document.source, file_path=document.path, schedule=[]
            )
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
            return False
        self.update_modules(file_path, build, ALev.QUICK, refresh=True)
        return len(self.modules[file_path].errors) == 0

    def deep_check(self, file_path: str) -> bool:
        """Rebuild a file and its dependencies."""
        if file_path not in self.modules:
            self.quick_check(file_path)
        try:
            file_path = self.unwind_to_parent(file_path)
            build = jac_ir_to_pass(ir=self.modules[file_path].ir)
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
            return False
        self.update_modules(file_path, build, ALev.DEEP)
        return len(self.modules[file_path].errors) == 0

    def type_check(self, file_path: str) -> bool:
        """Rebuild a file and its dependencies."""
        if file_path not in self.modules:
            self.deep_check(file_path)
        try:
            file_path = self.unwind_to_parent(file_path)
            build = jac_ir_to_pass(
                ir=self.modules[file_path].ir, schedule=type_checker_sched
            )
        except Exception as e:
            self.log_error(f"Error during type check: {e}")
            return False
        self.update_modules(file_path, build, ALev.TYPE)
        return len(self.modules[file_path].errors) == 0

    async def analyze_and_publish(self, uri: str, level: int = 2) -> None:
        """Analyze and publish diagnostics."""
        self.log_py(f"Analyzing {uri}...")
        success = await asyncio.get_event_loop().run_in_executor(
            self.executor, self.quick_check, uri
        )
        await self.push_diagnostics(uri)
        if success and level > 0:
            success = await asyncio.get_event_loop().run_in_executor(
                self.executor, self.deep_check, uri
            )
            await self.push_diagnostics(uri)
            if level > 1:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.type_check, uri
                )
                await self.push_diagnostics(uri)

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
        node_selected = find_deepest_symbol_node_at_pos(
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

    def get_node_info(self, node: ast.AstSymbolNode) -> Optional[str]:
        """Extract meaningful information from the AST node."""
        try:
            if isinstance(node, ast.NameAtom):
                node = node.name_of
            access = node.sym.access.value + " " if node.sym else None
            node_info = (
                f"({access if access else ''}{node.sym_category.value}) {node.sym_name}"
            )
            if node.name_spec.clean_type:
                node_info += f": {node.name_spec.clean_type}"
            if isinstance(node, ast.AstSemStrNode) and node.semstr:
                node_info += f"\n{node.semstr.value}"
            if isinstance(node, ast.AstDocNode) and node.doc:
                node_info += f"\n{node.doc.value}"
            if isinstance(node, ast.Ability) and node.signature:
                node_info += f"\n{node.signature.unparse()}"
            self.log_py(f"mypy_node: {node.gen.mypy_ast}")
        except AttributeError as e:
            self.log_warning(f"Attribute error when accessing node attributes: {e}")
        return node_info.strip()

    def get_document_symbols(self, file_path: str) -> list[lspt.DocumentSymbol]:
        """Return document symbols for a file."""
        if file_path in self.modules and (
            root_node := self.modules[file_path].ir._sym_tab
        ):
            return collect_symbols(root_node)
        return []

    def get_definition(
        self, file_path: str, position: lspt.Position
    ) -> Optional[lspt.Location]:
        """Return definition location for a file."""
        node_selected: Optional[ast.AstSymbolNode] = find_deepest_symbol_node_at_pos(
            self.modules[file_path].ir, position.line, position.character
        )
        if node_selected:
            if (
                isinstance(node_selected, ast.Name)
                and node_selected.parent
                and isinstance(node_selected.parent, ast.ModulePath)
            ):
                spec = get_mod_path(node_selected.parent, node_selected)
                if spec:
                    return lspt.Location(
                        uri=uris.from_fs_path(spec),
                        range=lspt.Range(
                            start=lspt.Position(line=0, character=0),
                            end=lspt.Position(line=0, character=0),
                        ),
                    )
                else:
                    return None
            elif node_selected.parent and isinstance(
                node_selected.parent, ast.ModuleItem
            ):
                path_range = get_item_path(node_selected.parent)
                if path_range:
                    path, range = path_range
                    if path and range:
                        return lspt.Location(
                            uri=uris.from_fs_path(path),
                            range=lspt.Range(
                                start=lspt.Position(line=range[0], character=0),
                                end=lspt.Position(line=range[1], character=5),
                            ),
                        )
                else:
                    return None
            elif isinstance(node_selected, (ast.ElementStmt, ast.BuiltinType)):
                return None
            decl_node = (
                node_selected.parent.body.target
                if node_selected.parent
                and isinstance(node_selected.parent, ast.AstImplNeedingNode)
                and isinstance(node_selected.parent.body, ast.AstImplOnlyNode)
                else (
                    node_selected.sym.decl
                    if (node_selected.sym and node_selected.sym.decl)
                    else node_selected
                )
            )
            self.log_py(f"{node_selected}, {decl_node}")
            decl_uri = uris.from_fs_path(decl_node.loc.mod_path)
            try:
                decl_range = create_range(decl_node.loc)
            except ValueError:  # 'print' name has decl in 0,0,0,0
                return None
            decl_location = lspt.Location(
                uri=decl_uri,
                range=decl_range,
            )

            return decl_location
        else:
            return None

    def get_references(
        self, file_path: str, position: lspt.Position
    ) -> list[lspt.Location]:
        """Return references for a file."""
        node_selected = find_deepest_symbol_node_at_pos(
            self.modules[file_path].ir, position.line, position.character
        )
        if node_selected and node_selected.sym:
            list_of_references: list[lspt.Location] = [
                lspt.Location(
                    uri=uris.from_fs_path(node.loc.mod_path),
                    range=create_range(node.loc),
                )
                for node in node_selected.sym.uses
            ]
            return list_of_references
        return []

    def get_semantic_tokens(self, file_path: str) -> lspt.SemanticTokens:
        """Return semantic tokens for a file."""
        if file_path not in self.modules:
            return lspt.SemanticTokens(data=[])
        return lspt.SemanticTokens(data=self.modules[file_path].sem_tokens)

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

    def log_py(self, message: str) -> None:
        """Log a message."""
        logging.info(message)
