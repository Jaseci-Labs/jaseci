import:py logging;
import:py from pygls.server, LanguageServer;
import:py lsprotocol.types as lspt;

with entry {
    server = LanguageServer("jac-lsp", "v0.1");
}

@server.feature(
    lspt.TEXT_DOCUMENT_COMPLETION,
    lspt.CompletionOptions(trigger_characters=[".", ":", ""])
)
can completions(params: lspt.CompletionParams) {
    logging.debug(
        f"{"Completion request: "}{params.text_document.uri}"
    );
    items = [];
    document = server.workspace.get_text_document(
        params.text_document.uri
    );
    current_line = document.lines[params.position.line].strip();
    if current_line.endswith("hello.") {
        items = [
            lspt.CompletionItem(label="world"),
            lspt.CompletionItem(label="friend")
        ];
    }

    return lspt.CompletionList(is_incomplete=False, items=items);
}

with entry {
    logging.debug("Starting server");
    server.start_io();
}

