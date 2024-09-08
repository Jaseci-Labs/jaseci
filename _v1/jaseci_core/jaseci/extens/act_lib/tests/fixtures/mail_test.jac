walker send_mail {
    can mail.send;
    with entry {
        mail.send(null, ["jaseci.dev@gmail.com"], "Test Subject", "Test", "<h1>Test</h1>");
    }
}