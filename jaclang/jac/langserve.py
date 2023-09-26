"""Example language server for JAC."""

from jaclang.vendor.pygls.lsp_types import (
    CompletionItem,
    CompletionList,
    CompletionParams,
    TEXT_DOCUMENT_COMPLETION,
)
from jaclang.vendor.pygls.server import LanguageServer


server = LanguageServer("example-server", "v0.1")


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams) -> CompletionList:
    """Provide completions for the current line."""
    items = []
    document = server.workspace.get_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    if current_line.endswith("hello."):
        items = [
            CompletionItem(label="world"),
            CompletionItem(label="friend"),
        ]
    return CompletionList(is_incomplete=False, items=items)
