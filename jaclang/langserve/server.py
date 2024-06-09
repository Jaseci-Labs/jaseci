"""Jaclang Language Server."""

from __future__ import annotations

from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.langserve.utils import debounce, log, log_error
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt

server = LanguageServer("jac-lsp", "v0.1")


@server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
@debounce(0.3)
async def did_change(
    ls: LanguageServer, params: lspt.DidChangeTextDocumentParams
) -> None:
    """Check syntax on change."""
    document = ls.workspace.get_document(params.text_document.uri)
    try:
        result = jac_str_to_pass(
            jac_str=document.source,
            file_path=document.path,
            schedule=[],
        )
        if not result.errors_had and not result.warnings_had:
            ls.publish_diagnostics(document.uri, [])
        else:
            ls.publish_diagnostics(
                document.uri,
                [
                    lspt.Diagnostic(
                        range=lspt.Range(
                            start=lspt.Position(
                                line=error.loc.first_line, character=error.loc.col_start
                            ),
                            end=lspt.Position(
                                line=error.loc.last_line,
                                character=error.loc.col_end,
                            ),
                        ),
                        message=error.msg,
                        severity=lspt.DiagnosticSeverity.Error,
                    )
                    for error in result.errors_had
                ],
            )
    except Exception as e:
        log_error(ls, f"Error during syntax check: {e}")
        log(f"Error during syntax check: {e}")


@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""]),
)
def completions(params: lspt.CompletionParams) -> lspt.CompletionList:
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
