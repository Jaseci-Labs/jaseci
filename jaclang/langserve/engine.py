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
from jaclang.compiler.passes.transform import Alert
from jaclang.langserve.utils import (
    collect_all_symbols_in_scope,
    collect_symbols,
    create_range,
    find_node_by_position,
    gen_diagnostics,
    get_item_path,
    get_mod_path,
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
        errors: list[Alert],
        warnings: list[Alert],
        parent: Optional[ModuleInfo] = None,
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.parent: Optional[ModuleInfo] = parent
        self.sem_tokens: list[int] = self.gen_sem_tokens()
        self.static_sem_tokens: List[Tuple[int, int, int, int, ast.AstSymbolNode]] = (
            self.gen_sem_tok_node()
        )

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

    def gen_sem_tok_node(self) -> List[Tuple[int, int, int, int, ast.AstSymbolNode]]:
        """Return semantic tokens."""
        tokens: List[Tuple[int, int, int, int, ast.AstSymbolNode]] = []
        for node in self.ir._in_mod_nodes:
            if isinstance(node, ast.NameAtom) and node.sem_token:
                line, col_start, col_end = (
                    node.loc.first_line - 1,
                    node.loc.col_start - 1,
                    node.loc.col_end - 1,
                )
                length = col_end - col_start
                tokens += [(line, col_start, col_end, length, node)]
        return tokens

    def get_token_start(self, token_index: int | None) -> tuple[int, int, int]:
        """Return the starting position of a token."""
        if token_index is None or token_index >= len(self.sem_tokens):
            logging.info(f"Token index: {token_index} is None or out of range")
            return 0, 0, 0
        
        current_line = 0
        current_char = 0
        current_tok_index = 0

        while current_tok_index < len(self.sem_tokens):
            token_line_delta = self.sem_tokens[current_tok_index]
            token_start_char = self.sem_tokens[current_tok_index + 1]

            if token_line_delta > 0:
                current_line += token_line_delta
                current_char = 0
            if current_tok_index == token_index:
                if token_line_delta > 0:
                    return (
                        current_line,
                        token_start_char,
                        token_start_char + self.sem_tokens[current_tok_index + 2],
                    )
                return (
                    current_line,
                    current_char + token_start_char,
                    current_char
                    + token_start_char
                    + self.sem_tokens[current_tok_index + 2],
                )

            current_char += token_start_char
            current_tok_index += 5

        return (
            current_line,
            current_char,
            current_char + self.sem_tokens[current_tok_index + 2],
        )

    def update_sem_tokens(
        self, content_changes: lspt.DidChangeTextDocumentParams, ls
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

            def find_surrounding_tokens(
                change_start_line: int,
                change_start_char: int,
                change_end_line: int,
                change_end_char: int,
            ) -> tuple[int | None, int | None, bool]:
                """Find the indices of the previous and next tokens surrounding the change."""
                prev_token_index = None
                next_token_index = None
                inside_tok = False
                for i, tok in enumerate(
                    [
                        self.get_token_start(i)
                        for i in range(0, len(self.sem_tokens), 5)
                    ][0:]
                ):
                    if (
                        not (prev_token_index is None or next_token_index is None)
                    ) and (
                        tok[0] > change_end_line
                        or (tok[0] == change_end_line and tok[1] > change_end_char)
                    ):
                        prev_token_index = i * 5
                        break
                    elif (
                        change_start_line == tok[0] == change_end_line
                        and tok[1] <= change_start_char
                        and tok[2] >= change_end_char
                    ):
                        prev_token_index = i * 5
                        inside_tok = True
                        break
                    elif (tok[0] < change_start_line) or (
                        tok[0] == change_start_line and tok[1] < change_start_char
                    ):
                        prev_token_index = i * 5
                    elif (tok[0] > change_end_line) or (
                        tok[0] == change_end_line and tok[1] > change_end_char
                    ):
                        next_token_index = i * 5
                        break

                return prev_token_index, next_token_index, inside_tok

            prev_token_index, next_token_index, insert_inside_token = (
                find_surrounding_tokens(
                    change_start_line,
                    change_start_char,
                    change_end_line,
                    change_end_char,
                )
            )
            if prev_token_index is not  None or next_token_index is not  None:
                prev_tok_pos = self.get_token_start(prev_token_index)
                nxt_tok_pos = self.get_token_start(next_token_index)
            changing_line_text = ls.get_line_of_code(
                content_changes.text_document.uri, change_start_line
            )

            insert_between_tokens = bool(
                (
                    change_start_line > prev_tok_pos[0]
                    or (
                        change_start_line == prev_tok_pos[0]
                        and change_start_char
                        > prev_tok_pos[1]
                        + self.sem_tokens[prev_token_index + 2]
                        if prev_token_index
                        and prev_token_index + 2 < len(self.sem_tokens)
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
            if is_delete:
                next_token_index = (
                    prev_token_index + 5
                    if next_token_index - prev_token_index == 10
                    else next_token_index
                )
                is_single = change_end_line == change_start_line
                is_next_token_same_line = (
                    change_end_line == nxt_tok_pos[0]
                )
                if is_single and insert_inside_token:
                    self.sem_tokens[prev_token_index + 2] -= change.range_length
                elif is_single and insert_between_tokens:
                    if is_next_token_same_line:
                        self.sem_tokens[next_token_index + 1] -= change.range_length
                    else:
                        self.sem_tokens[next_token_index] -= (
                            change_end_line - change_start_line
                        )
                elif insert_between_tokens:
                    if is_next_token_same_line:
                        char_del = (
                            nxt_tok_pos[1] - change_end_char
                        )
                        total_char_del = change_start_char + char_del
                        self.sem_tokens[next_token_index + 1] = (
                            (total_char_del - prev_tok_pos[1])
                            if prev_tok_pos[0]
                            == change_start_line
                            else total_char_del
                        )
                    self.sem_tokens[next_token_index] -= (
                        change_end_line - change_start_line
                    )
                return self.sem_tokens

            text = r"%s" % change.text
            line_delta = len(text.split("\n")) - 1
            multi_line_insertion = line_delta > 0
            if insert_inside_token and prev_token_index is not None:
                for i in ["\n", " ", "\t"]:
                    if i in change.text:
                        if (
                            prev_tok_pos[1]
                            == change_start_char
                        ):
                            if i == "\n":
                                self.sem_tokens[prev_token_index] += 1
                                self.sem_tokens[prev_token_index + 1] = (
                                    changing_line_text[1]
                                )
                            else:
                                self.sem_tokens[prev_token_index + 1] += len(
                                    change.text
                                )
                            return self.sem_tokens
                        else:
                            return self.sem_tokens
                index_offset = 2
                self.sem_tokens[prev_token_index + index_offset] += len(change.text)
                if (
                    prev_tok_pos[0]
                    == self.get_token_start(prev_token_index + 5)[0]
                ):
                    self.sem_tokens[prev_token_index + index_offset + 4] += len(
                        change.text
                    )
            if insert_between_tokens:
                both_tokens_in_same_line = (
                    prev_tok_pos[0]
                    == nxt_tok_pos[0]
                )
                if insert_between_tokens and multi_line_insertion:
                    if both_tokens_in_same_line:
                        char_del = (
                            nxt_tok_pos[1] - change_end_char
                        )
                        total_char_del = changing_line_text[1] + char_del
                    else:
                        is_prev_token_same_line = (
                            change_end_line == prev_tok_pos[0]
                        )
                        is_next_token_same_line = (
                            change_start_line
                            == nxt_tok_pos[0]
                        )
                        if is_prev_token_same_line:
                            total_char_del = nxt_tok_pos[1]
                        elif is_next_token_same_line:
                            char_del = (
                                nxt_tok_pos[1]
                                - change_end_char
                            )
                            total_char_del = changing_line_text[1] + char_del
                        else:
                            total_char_del = self.sem_tokens[next_token_index + 1]
                            line_delta -= change_end_line - change_start_line
                    self.sem_tokens[next_token_index + 1] = total_char_del
                    self.sem_tokens[next_token_index] += line_delta
                elif insert_between_tokens:
                    if both_tokens_in_same_line:
                        self.sem_tokens[next_token_index + 1] += len(change.text)
                        self.sem_tokens[next_token_index] += line_delta
                    else:
                        is_next_token_same_line = (
                            change_start_line
                            == nxt_tok_pos[0]
                        )
                        if is_next_token_same_line:
                            self.sem_tokens[next_token_index] += line_delta
                            self.sem_tokens[next_token_index + 1] += len(change.text)
                        else:
                            self.sem_tokens[next_token_index] += line_delta
        return self.sem_tokens


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self) -> None:
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}
        self.executor = ThreadPoolExecutor()
        self.tasks: dict[str, asyncio.Task] = {}

    def get_line_of_code(
        self, file_path: str, line_number: int
    ) -> Optional[tuple[str | None, int | None]]:
        """Return the line of code and the first non-space character position."""
        document = self.workspace.get_text_document(file_path)
        lines = document.source.splitlines()
        if 0 <= line_number < len(lines):
            line = lines[line_number].rstrip("\n")
            first_non_space_char_pos = len(line) - len(line.lstrip())
            return line, first_non_space_char_pos

        return None, None

    def update_modules(
        self, file_path: str, build: Pass, refresh: bool = False
    ) -> None:
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
        )
        for p in build.ir.mod_deps.keys():
            uri = uris.from_fs_path(p)
            self.modules[uri] = ModuleInfo(
                ir=build.ir.mod_deps[p],
                errors=[i for i in build.errors_had if i.loc.mod_path == p],
                warnings=[i for i in build.warnings_had if i.loc.mod_path == p],
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

    def find_index(
        self, sem_tokens: list[int], line: int, char: int, file_path: str
    ) -> Optional[int]:
        """Find index."""
        index = None
        for i, j in enumerate(
            [
                self.modules[file_path].get_token_start(i)
                for i in range(0, len(sem_tokens), 5)
            ]
        ):
            if j[0] == line and j[1] <= char <= j[2]:
                return i

        return index

    def get_hover_info(
        self, file_path: str, position: lspt.Position
    ) -> Optional[lspt.Hover]:
        """Return hover information for a file."""
        if file_path not in self.modules:
            return None
        token_index = self.find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
            file_path,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].static_sem_tokens[token_index][4]
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
        token_index = self.find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
            file_path,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].static_sem_tokens[token_index][4]
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
        index1 = self.find_index(
            self.modules[file_path].sem_tokens,
            position.line,
            position.character,
            file_path,
        )
        logging.info(f"index1:.... {index1}")
        if index1 is None:
            return []
        node_selected = self.modules[file_path].static_sem_tokens[index1][4]
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
