walker send_mail {
    can mail.send;
    with entry {
        mail.send(null, ["alexie.madolid@bcstechnology.com.au"], "Test Subject", "Test", "<h1>Test</h1>");
    }
}