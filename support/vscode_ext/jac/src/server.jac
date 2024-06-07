import:py logging;
import:py from pygls.server, LanguageServer;
import:py lsprotocol.types as lspt;

import:py from jaclang.compiler.passes.tool,
               FuseCommentsPass,
               JacFormatPass;

import:py from jaclang.compiler.compile,
               jac_str_to_pass;

with entry {
    server = LanguageServer("jac-lsp", "v0.1");
}

can log_error(ls: LanguageServer, message: str) -> None {
    ls.show_message_log(message, lsp.MessageType.Error);
    ls.show_message(message, lsp.MessageType.Error);
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

@server.feature(lspt.TEXT_DOCUMENT_FORMATTING)
can formatting(ls: LanguageServer, params: lspt.DocumentFormattingParams) -> lspt.List[lspt.TextEdit] {
    try {
        source = ls.workspace.get_text_document(params.text_document.uri).source;
        formatted_text = jac_str_to_pass(
            jac_str=source,
            file_path="",
            target=JacFormatPass,
            schedule=[FuseCommentsPass, JacFormatPass]
        ).ir.gen.jac;
    } except Exception as e {
        log_error(ls, f"Error during formatting: {e}");
        formatted_text = source;
    }
    return [
            lspt.TextEdit(
            range=lspt.Range(
                start=lspt.Position(line=0, character=0),
                end=lspt.Position(line=len(formatted_text), character=0)
            ),
            new_text=formatted_text
        )
    ];
}

with entry {
    logging.debug("Starting server");
    server.start_io();
}

