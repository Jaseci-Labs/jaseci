"""Living Workspace of Jac project."""

from __future__ import annotations

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes.main import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.compiler.unitree import UniScopeNode
from jaclang.langserve.sem_manager import SemTokManager
from jaclang.langserve.utils import (
    add_unique_text_edit,
    collect_all_symbols_in_scope,
    collect_child_tabs,
    create_range,
    find_deepest_symbol_node_at_pos,
    find_index,
    gen_diagnostics,
    get_symbols_for_outline,
    parse_symbol_path,
)
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self,
        ir: uni.Module,
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.sem_manager = SemTokManager(ir=ir)
        self.is_modified: bool = False

    @property
    def uri(self) -> str:
        """Return uri."""
        return uris.from_fs_path(self.ir.loc.mod_path)


class JacLangServer(LanguageServer):
    """Class for managing workspace."""

    def __init__(self) -> None:
        """Initialize workspace."""
        super().__init__("jac-lsp", "v0.1")
        self.modules: dict[str, ModuleInfo] = {}
        self.executor = ThreadPoolExecutor()
        self.tasks: dict[str, asyncio.Task] = {}
        self.program = JacProgram()

    def update_modules(
        self, file_path: str, build: uni.Module, refresh: bool = False
    ) -> None:
        """Update modules."""
        if not isinstance(build, uni.Module):
            self.log_error("Error with module build.")
            return
        self.modules[file_path] = ModuleInfo(ir=build)
        for p in self.program.mod.hub.keys():
            uri = uris.from_fs_path(p)
            if file_path != uri:
                self.modules[uri] = ModuleInfo(ir=self.program.mod.hub[p])

    def quick_check(self, file_path: str) -> bool:
        """Rebuild a file."""
        try:
            document = self.workspace.get_text_document(file_path)
            self.program.compile_from_str(
                source_str=document.source,
                file_path=document.path,
                mode=CMode.PARSE,
            )
            self.publish_diagnostics(
                file_path,
                gen_diagnostics(
                    file_path, self.program.errors_had, self.program.warnings_had
                ),
            )
            return len(self.program.errors_had) == 0
        except Exception as e:
            self.log_error(f"Error during syntax check: {e}")
            return False

    def deep_check(self, file_path: str, annex_view: Optional[str] = None) -> bool:
        """Rebuild a file and its dependencies."""
        try:
            start_time = time.time()
            document = self.workspace.get_text_document(file_path)
            if file_path in self.modules:
                return self.deep_check(
                    uris.from_fs_path(file_path), annex_view=file_path
                )
            self.program = JacProgram()  # TODO: Remove this Hack
            build = self.program.compile_from_str(
                source_str=document.source,
                file_path=document.path,
                mode=CMode.TYPECHECK,
            )
            self.update_modules(file_path, build)
            if discover := self.modules[file_path].ir.annexable_by:
                return self.deep_check(
                    uris.from_fs_path(discover), annex_view=file_path
                )

            self.publish_diagnostics(
                annex_view if annex_view else file_path,
                gen_diagnostics(
                    annex_view if annex_view else file_path,
                    self.program.errors_had,
                    self.program.warnings_had,
                ),
            )
            if annex_view:
                self.publish_diagnostics(
                    file_path,
                    gen_diagnostics(
                        file_path,
                        self.program.errors_had,
                        self.program.warnings_had,
                    ),
                )
            self.log_py(f"PROFILE: Deep check took {time.time() - start_time} seconds.")
            return len(self.program.errors_had) == 0
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
    ) -> lspt.CompletionList:  # TODO : need to refactor this
        """Return completion for a file."""
        document = self.workspace.get_text_document(file_path)
        mod_ir = self.modules[file_path].ir
        current_line = document.lines[position.line]
        current_pos = position.character
        current_symbol_path = parse_symbol_path(current_line, current_pos)
        builtin_mod = next(
            mod for name, mod in self.program.mod.hub.items() if "builtins" in name
        )
        builtin_tab = builtin_mod.sym_tab
        assert isinstance(builtin_tab, UniScopeNode)
        completion_items = []

        node_selected = find_deepest_symbol_node_at_pos(
            mod_ir,
            position.line,
            position.character - 2,
        )
        mod_tab = mod_ir.sym_tab if not node_selected else node_selected.sym_tab
        current_symbol_table = mod_tab

        if completion_trigger == ".":
            if current_symbol_path:
                temp_tab = mod_tab
                for symbol in current_symbol_path:
                    if symbol == "self":
                        is_ability_def = (
                            temp_tab.nix_owner
                            if isinstance(temp_tab.nix_owner, uni.AbilityDef)
                            else temp_tab.nix_owner.find_parent_of_type(uni.AbilityDef)
                        )
                        if not is_ability_def:
                            archi_owner = mod_tab.nix_owner.find_parent_of_type(
                                uni.Architype
                            )
                            temp_tab = (
                                archi_owner.sym_tab
                                if archi_owner and archi_owner.sym_tab
                                else mod_tab
                            )
                            continue
                        else:
                            archi_owner = (
                                (
                                    is_ability_def.decl_link.find_parent_of_type(
                                        uni.Architype
                                    )
                                )
                                if is_ability_def.decl_link
                                else None
                            )
                            temp_tab = (
                                archi_owner.sym_tab
                                if archi_owner and archi_owner.sym_tab
                                else temp_tab
                            )
                            continue
                    symb = temp_tab.lookup(symbol)
                    if symb:
                        fetc_tab = symb.fetch_sym_tab
                        if fetc_tab:
                            temp_tab = fetc_tab
                        else:
                            temp_tab = (
                                symb.defn[0].type_sym_tab
                                if symb.defn[0].type_sym_tab
                                else temp_tab
                            )
                    else:
                        break
                completion_items += collect_all_symbols_in_scope(
                    temp_tab, up_tree=False
                )
                if (
                    isinstance(temp_tab.nix_owner, uni.Architype)
                    and temp_tab.nix_owner.base_classes
                ):
                    base = []
                    for base_name in temp_tab.nix_owner.base_classes.items:
                        if isinstance(base_name, uni.Name) and base_name.sym:
                            base.append(base_name.sym)
                    for base_class_symbol in base:
                        if base_class_symbol.fetch_sym_tab:
                            completion_items += collect_all_symbols_in_scope(
                                base_class_symbol.fetch_sym_tab,
                                up_tree=False,
                            )

        else:
            if node_selected and (
                node_selected.find_parent_of_type(uni.Architype)
                or node_selected.find_parent_of_type(uni.AbilityDef)
            ):
                self_symbol = [
                    lspt.CompletionItem(
                        label="self", kind=lspt.CompletionItemKind.Variable
                    )
                ]
            else:
                self_symbol = []

            completion_items += (
                collect_all_symbols_in_scope(current_symbol_table)
                + self_symbol
                + collect_child_tabs(builtin_tab)
            )
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
            formatted_text = JacProgram.jac_str_formatter(
                source_str=document.source, file_path=document.path
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
            self.modules[file_path].sem_manager.sem_tokens,
            position.line,
            position.character,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].sem_manager.static_sem_tokens[
            token_index
        ][3]
        value = self.get_node_info(node_selected) if node_selected else None
        if value:
            return lspt.Hover(
                contents=lspt.MarkupContent(
                    kind=lspt.MarkupKind.PlainText, value=f"{value}"
                ),
            )
        return None

    def get_node_info(self, node: uni.AstSymbolNode) -> Optional[str]:
        """Extract meaningful information from the AST node."""
        try:
            if isinstance(node, uni.NameAtom):
                node = node.name_of
            access = node.sym.access.value + " " if node.sym else None
            node_info = (
                f"({access if access else ''}{node.sym_category.value}) {node.sym_name}"
            )
            if node.name_spec.clean_type:
                node_info += f": {node.name_spec.clean_type}"
            if isinstance(node, uni.AstSemStrNode) and node.semstr:
                node_info += f"\n{node.semstr.value}"
            if isinstance(node, uni.AstDocNode) and node.doc:
                node_info += f"\n{node.doc.value}"
            if isinstance(node, uni.Ability) and node.signature:
                node_info += f"\n{node.signature.unparse()}"
            self.log_py(f"mypy_node: {node.gen.mypy_ast}")
        except AttributeError as e:
            self.log_warning(f"Attribute error when accessing node attributes: {e}")
        return node_info.strip()

    def get_outline(self, file_path: str) -> list[lspt.DocumentSymbol]:
        """Return document symbols for a file."""
        if file_path in self.modules and (
            root_node := self.modules[file_path].ir.sym_tab
        ):
            return get_symbols_for_outline(root_node)
        return []

    def get_definition(
        self, file_path: str, position: lspt.Position
    ) -> Optional[lspt.Location]:
        """Return definition location for a file."""
        if file_path not in self.modules:
            return None
        token_index = find_index(
            self.modules[file_path].sem_manager.sem_tokens,
            position.line,
            position.character,
        )
        if token_index is None:
            return None
        node_selected = self.modules[file_path].sem_manager.static_sem_tokens[
            token_index
        ][3]
        if node_selected:
            if (
                isinstance(node_selected, uni.Name)
                and node_selected.parent
                and isinstance(node_selected.parent, uni.ModulePath)
            ):
                spec = node_selected.parent.abs_path
                if spec:
                    spec = spec[5:] if spec.startswith("File:") else spec
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
                node_selected.parent, uni.ModuleItem
            ):
                path = (
                    node_selected.parent.abs_path
                    or node_selected.parent.from_mod_path.abs_path
                )
                loc_range = (0, 0, 0, 0)

                if path and loc_range:
                    path = path[5:] if path.startswith("File:") else path
                    return lspt.Location(
                        uri=uris.from_fs_path(path),
                        range=lspt.Range(
                            start=lspt.Position(
                                line=loc_range[0], character=loc_range[1]
                            ),
                            end=lspt.Position(
                                line=loc_range[2], character=loc_range[3]
                            ),
                        ),
                    )
            elif isinstance(node_selected, uni.ElementStmt):
                return None
            decl_node = (
                node_selected.parent.body.target
                if node_selected.parent
                and isinstance(node_selected.parent, uni.AstImplNeedingNode)
                and isinstance(node_selected.parent.body, uni.AstImplOnlyNode)
                else (
                    node_selected.sym.decl
                    if (node_selected.sym and node_selected.sym.decl)
                    else node_selected
                )
            )
            decl_uri = uris.from_fs_path(decl_node.loc.mod_path)
            try:
                decl_range = create_range(decl_node.loc)
            except ValueError:
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
            self.modules[file_path].sem_manager.sem_tokens,
            position.line,
            position.character,
        )
        if index1 is None:
            return []
        node_selected = self.modules[file_path].sem_manager.static_sem_tokens[index1][3]
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

    def rename_symbol(
        self, file_path: str, position: lspt.Position, new_name: str
    ) -> Optional[lspt.WorkspaceEdit]:
        """Rename a symbol in a file."""
        if file_path not in self.modules:
            return None
        index1 = find_index(
            self.modules[file_path].sem_manager.sem_tokens,
            position.line,
            position.character,
        )
        if index1 is None:
            return None
        node_selected = self.modules[file_path].sem_manager.static_sem_tokens[index1][3]
        if node_selected and node_selected.sym:
            changes: dict[str, list[lspt.TextEdit]] = {}
            for node in [
                *node_selected.sym.uses,
                node_selected.sym.defn[0],
            ]:
                key = uris.from_fs_path(node.loc.mod_path)
                new_edit = lspt.TextEdit(
                    range=create_range(node.loc),
                    new_text=new_name,
                )
                add_unique_text_edit(changes, key, new_edit)
            return lspt.WorkspaceEdit(changes=changes)
        return None

    def get_semantic_tokens(self, file_path: str) -> lspt.SemanticTokens:
        """Return semantic tokens for a file."""
        if file_path not in self.modules:
            return lspt.SemanticTokens(data=[])
        return lspt.SemanticTokens(data=self.modules[file_path].sem_manager.sem_tokens)

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
