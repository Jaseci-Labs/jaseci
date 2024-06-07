import:py logging;
import:py from pygls.server, LanguageServer;
import:py lsprotocol.types as lspt;

glob server = LanguageServer("jac-lsp", "v0.1");

can log_error(ls: LanguageServer, message: str) -> None {
    ls.show_message_log(message, lspt.MessageType.Error);
    ls.show_message(message, lspt.MessageType.Error);
}

@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""])
)
can completions(params: lspt.CompletionParams) -> None;

@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
can formatting(ls: LanguageServer, params: lspt.DocumentFormattingParams) -> lspt.List[lspt.TextEdit];

with entry {
    logging.debug("Starting server");
    server.start_io();
}
