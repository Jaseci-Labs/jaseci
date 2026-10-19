def:pub new_buf -> bytes {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub word_at(buf: bytes, off: int) -> int {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub put_word(buf: bytes, off: int, v: int) -> bytes {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub get_attrs(fd: int) -> tuple[(bytes, int)] {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub set_attrs(fd: int, when: int, blob: bytes) -> int {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub in_speed(buf: bytes) -> int {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub out_speed(buf: bytes) -> int {
    raise RuntimeError("termios is unavailable on this platform");
}

def:pub set_speeds(buf: bytes, ispeed: int, ospeed: int) -> int {
    raise RuntimeError("termios is unavailable on this platform");
}
