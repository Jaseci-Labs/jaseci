impl user_home(name: str) -> str | None {
    if "\x00" in name {
        raise ValueError("embedded null byte");
    }
    buffer = b"\x00" * 4096;
    length = __jac_home_dir(name, buffer, 4096);
    if length == -1 {
        return None;
    }
    if length < 0 {
        return "";
    }
    return buffer[:length].decode("utf-8");
}
