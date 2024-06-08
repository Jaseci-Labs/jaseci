"""Jaclang Language Server."""

from __future__ import annotations

from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt

server = LanguageServer("jac-lsp", "v0.1")


def log_error(ls: LanguageServer, message: str) -> None:
    """Log an error message."""
    ls.show_message_log(message, lspt.MessageType.Error)
    ls.show_message(message, lspt.MessageType.Error)


# @server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
# def did_change(ls: LanguageServer, params: lspt.DidChangeTextDocumentParams) -> None:
#     pass


@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""]),
)
def completions(params: lspt.CompletionParams) -> None:
    """Provide completions for the given completion request."""
    items = []
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    if current_line.endswith("hello."):

        items = [
            lspt.CompletionItem(label="world"),
            lspt.CompletionItem(label="friend"),
        ]
    return lspt.CompletionList(is_incomplete=False, items=items)


@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
def formatting(
    ls: LanguageServer, params: lspt.DocumentFormattingParams
) -> lspt.List[lspt.TextEdit]:
    """Format the given document."""
    try:
        source = ls.workspace.get_text_document(params.text_document.uri).source
        formatted_text = jac_str_to_pass(
            jac_str=source,
            file_path="",
            target=JacFormatPass,
            schedule=[FuseCommentsPass, JacFormatPass],
        ).ir.gen.jac
    except Exception as e:
        log_error(ls, f"Error during formatting: {e}")
        formatted_text = source
    return [
        lspt.TextEdit(
            range=lspt.Range(
                start=lspt.Position(line=0, character=0),
                end=lspt.Position(line=len(formatted_text), character=0),
            ),
            new_text=formatted_text,
        )
    ]


def run_lang_server() -> None:
    """Run the language server."""
    server.start_io()
