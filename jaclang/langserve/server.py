"""Jaclang Language Server."""

from __future__ import annotations

from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.langserve.engine import JacLangServer
from jaclang.langserve.utils import debounce, log_error

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
    try:
        document = ls.workspace.get_document(params.text_document.uri)
        formatted_text = jac_str_to_pass(
            jac_str=document.source,
            file_path=document.path,
            target=JacFormatPass,
            schedule=[FuseCommentsPass, JacFormatPass],
        ).ir.gen.jac
    except Exception as e:
        log_error(ls, f"Error during formatting: {e}")
        formatted_text = document.source
    return [
        lspt.TextEdit(
            range=lspt.Range(
                start=lspt.Position(line=0, character=0),
                end=lspt.Position(
                    line=len(formatted_text.splitlines()) + 1, character=0
                ),
            ),
            new_text=formatted_text,
        )
    ]


def run_lang_server() -> None:
    """Run the language server."""
    server.start_io()


if __name__ == "__main__":
    run_lang_server()
