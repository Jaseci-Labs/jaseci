"""Living Workspace of Jac project."""

from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional, Tuple

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.langserve.utils import (
    collect_all_symbols_in_scope,
    collect_symbols,
    create_range,
    find_index,
    find_node_by_position,
    find_surrounding_tokens,
    gen_diagnostics,
    get_item_path,
    get_line_of_code,
    get_mod_path,
    get_token_start,
    parse_symbol_path,
    resolve_completion_symbol_table,
)
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: ast.Module,
        impl_parent: Optional[ModuleInfo] = None,
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.impl_parent: Optional[ModuleInfo] = impl_parent
        self.sem_tokens: list[int] = self.gen_sem_tokens()
        self.static_sem_tokens: List[
            Tuple[lspt.Position, int, int, ast.AstSymbolNode]
        ] = self.gen_sem_tok_node()

    @property
    def uri(self) -> str:
        """Return uri."""
        return uris.from_fs_path(self.ir.loc.mod_path)

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

    def gen_sem_tok_node(
        self,
    ) -> List[Tuple[lspt.Position, int, int, ast.AstSymbolNode]]:
        """Return semantic tokens."""
        tokens: List[Tuple[lspt.Position, int, int, ast.AstSymbolNode]] = []
        for node in self.ir._in_mod_nodes:
            if isinstance(node, ast.NameAtom) and node.sem_token:
                line, col_start, col_end = (
                    node.loc.first_line - 1,
                    node.loc.col_start - 1,
                    node.loc.col_end - 1,
                )
                length = col_end - col_start
                pos = lspt.Position(line, col_start)
                tokens += [(pos, col_end, length, node)]
        return tokens

    def update_sem_tokens(
        self,
        content_changes: lspt.DidChangeTextDocumentParams,
        sem_tokens: list[int],
        document_lines: List[str],
    ) -> list[int]:
        """Update semantic tokens on change."""
        for change in [
            x
            for x in content_changes.content_changes
            if isinstance(x, lspt.TextDocumentContentChangeEvent_Type1)
        ]:
            change_start_line = change.range.start.line
            change_start_char = change.range.start.character
            change_end_line = change.range.end.line
            change_end_char = change.range.end.character

            is_delete = change.text == ""
            prev_token_index, next_token_index, insert_inside_token = (
                find_surrounding_tokens(
                    change_start_line,
                    change_start_char,
                    change_end_line,
                    change_end_char,
                    sem_tokens,
                )
            )
            prev_tok_pos = get_token_start(prev_token_index, sem_tokens)
            nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
            changing_line_text = get_line_of_code(change_start_line, document_lines)
            if not changing_line_text:
                return sem_tokens
            is_edit_between_tokens = bool(
                (
                    change_start_line > prev_tok_pos[0]
                    or (
                        change_start_line == prev_tok_pos[0]
                        and change_start_char
                        > prev_tok_pos[1] + sem_tokens[prev_token_index + 2]
                        if prev_token_index and prev_token_index + 2 < len(sem_tokens)
                        else 0
                    )
                )
                and (
                    change_end_line < nxt_tok_pos[0]
                    or (
                        change_end_line == nxt_tok_pos[0]
                        and change_end_char < nxt_tok_pos[1]
                    )
                )
            )
            text = r"%s" % change.text
            line_delta = len(text.split("\n")) - 1
            is_multiline_insertion = line_delta > 0
            # logging.info(f"chnge text: {change}")
            # logging.info(
            #     f"""\n\nprev_token_index: {prev_token_index}, next_token_index:{next_token_index}
            #     ,\n insert_inside_token: {insert_inside_token}, insert_between_tokens:
            # {is_edit_between_tokens},\n multi_line_insertion:  {is_multiline_insertion}\n\n"""
            # )
            if is_delete:
                next_token_index = (
                    prev_token_index + 5
                    if insert_inside_token
                    and prev_token_index is not None
                    or (
                        next_token_index
                        and prev_token_index is not None
                        and next_token_index >= 10
                        and next_token_index - prev_token_index == 10
                    )
                    else next_token_index
                )
                if next_token_index is None:
                    return sem_tokens
                nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
                is_single_line_change = change_end_line == change_start_line
                is_next_token_same_line = change_end_line == nxt_tok_pos[0]
                if (
                    is_single_line_change
                    and insert_inside_token
                    and prev_token_index is not None
                ):
                    sem_tokens[prev_token_index + 2] -= change.range_length
                    if is_next_token_same_line:
                        sem_tokens[next_token_index + 1] -= change.range_length
                elif is_single_line_change and is_edit_between_tokens:
                    if is_next_token_same_line:
                        sem_tokens[next_token_index + 1] -= change.range_length

                    else:
                        sem_tokens[next_token_index] -= (
                            change_end_line - change_start_line
                        )
                else:
                    if is_next_token_same_line:
                        char_del = nxt_tok_pos[1] - change_end_char
                        total_char_del = change_start_char + char_del
                        sem_tokens[next_token_index + 1] = (
                            (total_char_del - prev_tok_pos[1])
                            if prev_tok_pos[0] == change_start_line
                            else total_char_del
                        )
                    sem_tokens[next_token_index] -= change_end_line - change_start_line
                return sem_tokens

            is_token_boundary_edit = False
            if insert_inside_token and prev_token_index is not None:
                for i in ["\n", " ", "\t"]:
                    if i in change.text:
                        if prev_tok_pos[1] == change_start_char:
                            if i == "\n":
                                sem_tokens[prev_token_index] += line_delta
                                sem_tokens[prev_token_index + 1] = changing_line_text[1]
                            else:
                                sem_tokens[prev_token_index + 1] += len(change.text)
                            return sem_tokens
                        else:
                            is_token_boundary_edit = True
                            next_token_index = prev_token_index + 5
                            nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
                            break
                if not is_token_boundary_edit:
                    selected_region = change_end_char - change_start_char
                    index_offset = 2
                    sem_tokens[prev_token_index + index_offset] += (
                        len(change.text) - selected_region
                    )
                    if (
                        prev_tok_pos[0]
                        == get_token_start(prev_token_index + 5, sem_tokens)[0]
                    ):
                        sem_tokens[prev_token_index + index_offset + 4] += (
                            len(change.text) - selected_region
                        )

            tokens_on_same_line = prev_tok_pos[0] == nxt_tok_pos[0]
            if (
                is_edit_between_tokens
                or is_token_boundary_edit
                or is_multiline_insertion
            ) and next_token_index is not None:
                if is_multiline_insertion:
                    if tokens_on_same_line:
                        char_del = nxt_tok_pos[1] - change_end_char
                        total_char_del = changing_line_text[1] + char_del

                    else:
                        is_prev_token_same_line = change_end_line == prev_tok_pos[0]
                        is_next_token_same_line = change_start_line == nxt_tok_pos[0]
                        if is_prev_token_same_line:
                            total_char_del = nxt_tok_pos[1]
                        elif is_next_token_same_line:
                            char_del = nxt_tok_pos[1] - change_end_char
                            total_char_del = changing_line_text[1] + char_del
                        else:
                            total_char_del = sem_tokens[next_token_index + 1]
                            line_delta -= change_end_line - change_start_line
                    sem_tokens[next_token_index + 1] = total_char_del
                    sem_tokens[next_token_index] += line_delta
                else:
                    if tokens_on_same_line:
                        sem_tokens[next_token_index + 1] += len(change.text)
                        sem_tokens[next_token_index] += line_delta
                    else:
                        is_next_token_same_line = change_start_line == nxt_tok_pos[0]
                        if is_next_token_same_line:
                            sem_tokens[next_token_index] += line_delta
                            sem_tokens[next_token_index + 1] += len(change.text)
                        else:
                            sem_tokens[next_token_index] += line_delta
        return sem_tokens


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self) -> None:
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}
        self.executor = ThreadPoolExecutor()
        self.tasks: dict[str, asyncio.Task] = {}

    def update_modules(
        self, file_path: str, build: Pass, refresh: bool = False
    ) -> None:
        """Update modules."""
        if not isinstance(build.ir, ast.Module):
            self.log_error("Error with module build.")
            return
        keep_parent = (
            self.modules[file_path].impl_parent if file_path in self.modules else None
        )
        self.modules[file_path] = ModuleInfo(ir=build.ir, impl_parent=keep_parent)
        for p in build.ir.mod_deps.keys():
            uri = uris.from_fs_path(p)
            if file_path != uri:
                self.modules[uri] = ModuleInfo(
                    ir=build.ir.mod_deps[p],
                    impl_parent=self.modules[file_path],
                )

    def quick_check(self, file_path: str) -> bool:
        """Rebuild a file."""
        try:
            document = self.workspace.get_text_document(file_path)
            build = jac_str_to_pass(
                jac_str=document.source, file_path=document.path, schedule=[]
            )
            self.publish_diagnostics(
                file_path,
                gen_diagnostics(file_path, build.errors_had, build.warnings_had),
            )
            return len(build.errors_had) == 0
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
            return False

    def deep_check(self, file_path: str, annex_view: Optional[str] = None) -> bool:
        """Rebuild a file and its dependencies."""
        try:
            document = self.workspace.get_text_document(file_path)
            if file_path in self.modules and (
                parent := self.modules[file_path].impl_parent
            ):
                return self.deep_check(
                    uris.from_fs_path(parent.ir.loc.mod_path), annex_view=file_path
                )
            build = jac_str_to_pass(
                jac_str=document.source,
                file_path=document.path,
                schedule=py_code_gen_typed,
            )
            self.update_modules(file_path, build)
            if discover := self.modules[file_path].ir.annexable_by:
                return self.deep_check(
                    uris.from_fs_path(discover), annex_view=file_path
                )

            self.publish_diagnostics(
                file_path,
                gen_diagnostics(
                    annex_view if annex_view else file_path,
                    build.errors_had,
                    build.warnings_had,
                ),
            )
            return len(build.errors_had) == 0
        except Exception as e:
            self.log_error(f"Error during deep check: {e}")
            return False

    async def launch_quick_check(self, uri: str) -> None:
        """Analyze and publish diagnostics."""
        await asyncio.get_event_loop().run_in_executor(
            self.executor, self.quick_check, uri
        )

    async def launch_deep_check(self, uri: str) -> None:
        """Analyze and publish diagnostics."""

        async def run_in_executor(
            func: Callable[[str, Optional[str]], bool],
            file_path: str,
            annex_view: Optional[str] = None,
        ) -> None:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, func, file_path, annex_view)

        if uri in self.tasks and not self.tasks[uri].done():
            self.log_py(f"Canceling {uri} deep check...")
            self.tasks[uri].cancel()
            del self.tasks[uri]
        self.log_py(f"Analyzing {uri}...")
        task = asyncio.create_task(run_in_executor(self.deep_check, uri))
        self.tasks[uri] = task
        await task

    def get_completion(
        self, file_path: str, position: lspt.Position, completion_trigger: Optional[str]
    ) -> lspt.CompletionList:
        """Return completion for a file."""
        completion_items = []
        document = self.workspace.get_text_document(file_path)
        current_line = document.lines[position.line]
        current_pos = position.character
        current_symbol_path = parse_symbol_path(current_line, current_pos)
        node_selected = find_node_by_position(
            self.modules[file_path].static_sem_tokens,
            position.line,
            position.character - 2,
        )

        mod_tab = (
            self.modules[file_path].ir.sym_tab
            if not node_selected
            else node_selected.sym_tab
        )
        current_tab = self.modules[file_path].ir._sym_tab
        current_symbol_table = mod_tab
        if completion_trigger == ".":
            completion_items = resolve_completion_symbol_table(
                mod_tab, current_symbol_path, current_tab
            )
        else:
            try:  # noqa SIM105
                completion_items = collect_all_symbols_in_scope(current_symbol_table)
            except AttributeError:
                pass
        return lspt.CompletionList(is_incomplete=False, items=completion_items)

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
        if file_path not in self.modules:
            return None
        token_index = find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].static_sem_tokens[token_index][3]
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
        if file_path not in self.modules:
            return None
        token_index = find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].static_sem_tokens[token_index][3]
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
        if file_path not in self.modules:
            return []
        index1 = find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
        )
        if index1 is None:
            return []
        node_selected = self.modules[file_path].static_sem_tokens[index1][3]
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
