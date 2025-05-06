import pygls.server;

obj ServerWrapper {
    def init(file: str);
    def get_server(server_ip: str, port: int) -> pygls.server.LanguageServer;
}

:obj:ServerWrapper:can:init
(file: str) {
    self.file = file;
}

:obj:ServerWrapper:can:get_server {
    return pygls.server.LanguageServer("test_server", "1");
}
