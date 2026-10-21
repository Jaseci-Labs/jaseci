impl user_home(name: str) -> str | None {
    if "\x00" in name {
        raise ValueError("embedded null byte");
    }
    size = 4096;
    while True {
        buffer = b"\x00" * size;
        length = __jac_home_dir(name, buffer, size);
        if length == -1 {
            return None;
        }
        if length < 0 {
            return "";
        }
        if length < size {
            return buffer[:length].decode("utf-8");
        }
        size = length + 1;
    }
}
