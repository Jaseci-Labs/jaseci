"""Jaclang Language Server."""

from __future__ import annotations

import threading
from typing import Optional

from jaclang.langserve.engine import JacLangServer
from jaclang.langserve.utils import debounce

import lsprotocol.types as lspt

server = JacLangServer()
analysis_thread: Optional[threading.Thread] = None
analysis_stop_event = threading.Event()


def analyze_and_publish(ls: JacLangServer, uri: str) -> None:
    """Analyze and publish diagnostics."""
    global analysis_thread, analysis_stop_event

    def run_analysis() -> None:
        ls.quick_check(uri)
        ls.push_diagnostics(uri)
        ls.deep_check(uri)
        ls.push_diagnostics(uri)
        ls.type_check(uri)
        ls.push_diagnostics(uri)

    analysis_thread = threading.Thread(target=run_analysis)
    analysis_thread.start()


def stop_analysis() -> None:
    """Stop analysis."""
    global analysis_thread, analysis_stop_event
    if analysis_thread is not None:
        analysis_stop_event.set()
        analysis_thread.join()
        analysis_stop_event.clear()


@server.feature(lspt.TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: JacLangServer, params: lspt.DidOpenTextDocumentParams) -> None:
    """Check syntax on change."""
    stop_analysis()
    analyze_and_publish(ls, params.text_document.uri)


@server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
@debounce(0.1)
async def did_change(
    ls: JacLangServer, params: lspt.DidChangeTextDocumentParams
) -> None:
    """Check syntax on change."""
    stop_analysis()
    analyze_and_publish(ls, params.text_document.uri)


@server.feature(lspt.TEXT_DOCUMENT_DID_SAVE)
async def did_save(ls: JacLangServer, params: lspt.DidSaveTextDocumentParams) -> None:
    """Check syntax on save."""
    stop_analysis()
    analyze_and_publish(ls, params.text_document.uri)


@server.feature(
    lspt.WORKSPACE_DID_CREATE_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
async def did_create_files(ls: JacLangServer, params: lspt.CreateFilesParams) -> None:
    """Check syntax on file creation."""
    for file in params.files:
        ls.quick_check(file.uri)
        ls.push_diagnostics(file.uri)


@server.feature(
    lspt.WORKSPACE_DID_RENAME_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
async def did_rename_files(ls: JacLangServer, params: lspt.RenameFilesParams) -> None:
    """Check syntax on file rename."""
    new_uris = [file.new_uri for file in params.files]
    old_uris = [file.old_uri for file in params.files]
    for i in range(len(new_uris)):
        ls.rename_module(old_uris[i], new_uris[i])
        ls.quick_check(new_uris[i])


@server.feature(
    lspt.WORKSPACE_DID_DELETE_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
async def did_delete_files(ls: JacLangServer, params: lspt.DeleteFilesParams) -> None:
    """Check syntax on file delete."""
    for file in params.files:
        ls.delete_module(file.uri)


@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""]),
)
async def completion(
    ls: JacLangServer, params: lspt.CompletionParams
) -> lspt.CompletionList:
    """Provide completion."""
    return ls.get_completion(params.text_document.uri, params.position)


@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
def formatting(
    ls: JacLangServer, params: lspt.DocumentFormattingParams
) -> list[lspt.TextEdit]:
    """Format the given document."""
    return ls.formatted_jac(params.text_document.uri)


# @server.feature(lspt.TEXT_DOCUMENT_HOVER, lspt.HoverOptions(work_done_progress=True))
def hover(
    ls: JacLangServer, params: lspt.TextDocumentPositionParams
) -> Optional[lspt.Hover]:
    """Provide hover information for the given hover request."""

    def get_value() -> Optional[str]:
        """Get value by using the position to get which AST node it falls under."""
        line = params.position.line
        character = params.position.character

        root_node = ls.modules[params.text_document.uri].ir
        deepest_node = None
        for node in ls.find_deepest_node(root_node, line, character):
            deepest_node = node

        import jaclang.compiler.absyntree as ast

        def get_node_info(node: ast.AstNode) -> Optional[str]:
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
                                    node_info = f"(architype) {node.value} \n{decl_node.doc.lit_value}"
                                else:
                                    node_info = f"(architype) {node.value}"
                            elif isinstance(decl_node, ast.Ability):
                                node_info = f"(ability) can {node.value}"
                                if decl_node.signature:
                                    node_info += f" {decl_node.signature.unparse()}"
                                if decl_node.doc:
                                    node_info += f"\n{decl_node.doc.lit_value}"
                            elif isinstance(decl_node, ast.Name):
                                node_info = f"{node.value}"
                            elif isinstance(decl_node, ast.HasVar):
                                if decl_node.type_tag:
                                    node_info = f"(variable) {decl_node.name.value} {decl_node.type_tag.unparse()}"
                                else:
                                    node_info = f"(variable) {decl_node.name.value}"
                            else:
                                ls.log_warning(
                                    f"no match found decl node is \n {decl_node}"
                                )
                        else:
                            node_info = f"Name: {node.value}\n"
                    else:
                        return None
                else:
                    # ls.log_warning(f'Something happened in function -[position_within_node] ')
                    return None
            except AttributeError as e:
                ls.log_error(f"Attribute error when accessing node attributes: {e}")
            return node_info.strip()

        if deepest_node:
            return get_node_info(deepest_node)
        return None

    value = get_value()
    if value:
        return lspt.Hover(
            contents=lspt.MarkupContent(
                kind=lspt.MarkupKind.PlainText, value=f"{value}"
            ),
        )
    return None


def run_lang_server() -> None:
    """Run the language server."""
    server.start_io()


if __name__ == "__main__":
    run_lang_server()
