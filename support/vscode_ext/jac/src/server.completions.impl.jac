:can:completions(params: lspt.CompletionParams) {
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