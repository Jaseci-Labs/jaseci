:can:completions(params: lspt.CompletionParams) {
    items = [];
    document = server.workspace.get_text_document(
        params.text_document.uri
    );
    current_line = document.lines[params.position.line].strip();
    if current_line.endswith("hello.") {
        log_error(server, "Hello!");
        items = [
            lspt.CompletionItem(label="world"),
            lspt.CompletionItem(label="friend")
        ];
    }

    return lspt.CompletionList(is_incomplete=False, items=items);
}