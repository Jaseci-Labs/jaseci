"""Jaclang Language Server."""

from __future__ import annotations


from jaclang.langserve.engine import JacLangServer
from jaclang.langserve.utils import debounce

import lsprotocol.types as lspt

server = JacLangServer()


@server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
@debounce(0.1)
async def did_change(
    ls: JacLangServer, params: lspt.DidChangeTextDocumentParams
) -> None:
    """Check syntax on change."""
    ls.quick_check(params.text_document.uri)
    ls.push_diagnostics(params.text_document.uri)


@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
def formatting(
    ls: JacLangServer, params: lspt.DocumentFormattingParams
) -> list[lspt.TextEdit]:
    """Format the given document."""
    return ls.formatted_jac(params.text_document.uri)


def run_lang_server() -> None:
    """Run the language server."""
    server.start_io()


if __name__ == "__main__":
    run_lang_server()
