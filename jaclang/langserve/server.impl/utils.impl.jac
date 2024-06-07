:can:log_error(ls: LanguageServer, message: str) -> None {
    ls.show_message_log(message, lspt.MessageType.Error);
    ls.show_message(message, lspt.MessageType.Error);
}
