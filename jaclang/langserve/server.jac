import:py from pygls.server, LanguageServer;
import:py lsprotocol.types as lspt;

glob server = LanguageServer("jac-lsp", "v0.1");

can log_error(ls: LanguageServer, message: str) -> None;

@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""])
)
can completions(params: lspt.CompletionParams) -> None;

@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
can formatting(ls: LanguageServer, params: lspt.DocumentFormattingParams) -> lspt.List[lspt.TextEdit];

with entry {
    server.start_io();
}