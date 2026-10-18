obj:pub HTTPResponse {
    has status: int,
        reason: str,
        _url: str,
        _body: bytes,
        _header_names: list[str],
        _header_values: list[str],
        _pos: int = 0;

    def read(amt: (int | None) = None) -> bytes;
    def getheader(name: str, `default: (str | None) = None) -> (str | None);
    def geturl -> str;
    def close;
}

impl HTTPResponse.read(amt: (int | None) = None) -> bytes {
    start = self._pos;
    end = len(self._body);
    if amt is not None and amt >= 0 and start + amt < end {
        end = start + amt;
    }
    self._pos = end;
    return self._body[start:end];
}

impl HTTPResponse.getheader(name: str, `default: (str | None) = None) -> (str | None) {
    wanted = name.lower();
    i: int = 0;
    while i < len(self._header_names) {
        if self._header_names[i] == wanted {
            return self._header_values[i];
        }
        i += 1;
    }
    return `default;
}

impl HTTPResponse.geturl -> str {
    return self._url;
}

impl HTTPResponse.close {
    return;
}
