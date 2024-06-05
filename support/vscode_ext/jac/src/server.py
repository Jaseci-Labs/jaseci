import logging
from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions,
    CompletionItem,
    CompletionList,
    CompletionParams,
)

server = LanguageServer("example-server", "v0.1")


@server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[".", ":", ""])
)
def completions(params: CompletionParams):
    logging.debug(f"Completion request: {params.text_document.uri}")
    items = []
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    if current_line.endswith("hello."):
        items = [
            CompletionItem(label="world"),
            CompletionItem(label="friend"),
        ]
    return CompletionList(is_incomplete=False, items=items)


logging.debug("Starting server")
# server.start_tcp(host="localhost", port=8080)
server.start_io()
