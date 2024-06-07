:can:formatting(ls: LanguageServer, params: lspt.DocumentFormattingParams) -> lspt.List[lspt.TextEdit] {
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