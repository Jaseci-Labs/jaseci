"""Jaclang Language Server."""

from __future__ import annotations

from typing import Optional

from jaclang.compiler.constant import (
    JacSemTokenModifier as SemTokMod,
    JacSemTokenType as SemTokType,
)
from jaclang.langserve.engine import JacLangServer

import lsprotocol.types as lspt

server = JacLangServer()


@server.feature(lspt.TEXT_DOCUMENT_DID_OPEN)
@server.feature(lspt.TEXT_DOCUMENT_DID_SAVE)
async def did_open(ls: JacLangServer, params: lspt.DidOpenTextDocumentParams) -> None:
    """Check syntax on change."""
    await ls.launch_deep_check(params.text_document.uri)
    ls.lsp.send_request(lspt.WORKSPACE_SEMANTIC_TOKENS_REFRESH)


@server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
async def did_change(
    ls: JacLangServer, params: lspt.DidChangeTextDocumentParams
) -> None:
    """Check syntax on change."""
    await ls.launch_quick_check(file_path := params.text_document.uri)
    if file_path in ls.modules:
        ls.modules[file_path].update_sem_tokens(params, ls)
        ls.lsp.send_request(lspt.WORKSPACE_SEMANTIC_TOKENS_REFRESH)


@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
def formatting(
    ls: JacLangServer, params: lspt.DocumentFormattingParams
) -> list[lspt.TextEdit]:
    """Format the given document."""
    return ls.formatted_jac(params.text_document.uri)


@server.feature(
    lspt.WORKSPACE_DID_CREATE_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
def did_create_files(ls: JacLangServer, params: lspt.CreateFilesParams) -> None:
    """Check syntax on file creation."""


@server.feature(
    lspt.WORKSPACE_DID_RENAME_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
def did_rename_files(ls: JacLangServer, params: lspt.RenameFilesParams) -> None:
    """Check syntax on file rename."""
    new_uris = [file.new_uri for file in params.files]
    old_uris = [file.old_uri for file in params.files]
    for i in range(len(new_uris)):
        ls.rename_module(old_uris[i], new_uris[i])


@server.feature(
    lspt.WORKSPACE_DID_DELETE_FILES,
    lspt.FileOperationRegistrationOptions(
        filters=[
            lspt.FileOperationFilter(pattern=lspt.FileOperationPattern("**/*.jac"))
        ]
    ),
)
def did_delete_files(ls: JacLangServer, params: lspt.DeleteFilesParams) -> None:
    """Check syntax on file delete."""
    for file in params.files:
        ls.delete_module(file.uri)


@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", "a-zA-Z0-9"]),
)
def completion(ls: JacLangServer, params: lspt.CompletionParams) -> lspt.CompletionList:
    """Provide completion."""
    return ls.get_completion(
        params.text_document.uri,
        params.position,
        params.context.trigger_character if params.context else None,
    )


@server.feature(lspt.TEXT_DOCUMENT_HOVER, lspt.HoverOptions(work_done_progress=True))
def hover(
    ls: JacLangServer, params: lspt.TextDocumentPositionParams
) -> Optional[lspt.Hover]:
    """Provide hover information for the given hover request."""
    return ls.get_hover_info(params.text_document.uri, params.position)


@server.feature(lspt.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbol(
    ls: JacLangServer, params: lspt.DocumentSymbolParams
) -> list[lspt.DocumentSymbol]:
    """Provide document symbols."""
    return ls.get_document_symbols(params.text_document.uri)


@server.feature(lspt.TEXT_DOCUMENT_DEFINITION)
def definition(
    ls: JacLangServer, params: lspt.TextDocumentPositionParams
) -> Optional[lspt.Location]:
    """Provide definition."""
    return ls.get_definition(params.text_document.uri, params.position)


@server.feature(lspt.TEXT_DOCUMENT_REFERENCES)
def references(ls: JacLangServer, params: lspt.ReferenceParams) -> list[lspt.Location]:
    """Provide references."""
    return ls.get_references(params.text_document.uri, params.position)


@server.feature(
    lspt.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    lspt.SemanticTokensLegend(
        token_types=SemTokType.as_str_list(),
        token_modifiers=SemTokMod.as_str_list(),
    ),
)
def semantic_tokens_full(
    ls: JacLangServer, params: lspt.SemanticTokensParams
) -> lspt.SemanticTokens:
    """Provide semantic tokens."""
    # import logging

    # logging.info("\nGetting semantic tokens\n")
    # # logging.info(ls.get_semantic_tokens(params.text_document.uri))
    # i = 0
    # while i < len(ls.get_semantic_tokens(params.text_document.uri).data):
    #     logging.info(ls.get_semantic_tokens(params.text_document.uri).data[i : i + 5])
    #     i += 5
    return ls.get_semantic_tokens(params.text_document.uri)


def run_lang_server() -> None:
    """Run the language server."""
    server.start_io()


if __name__ == "__main__":
    run_lang_server()
