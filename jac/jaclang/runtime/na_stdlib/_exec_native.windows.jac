import from c { def __jac_win_executable_path(buf: bytes, size: int) -> int;  }

"""The path of the running image, from the Windows floor."""
def:pub executable_path -> str {
    buf = b"\x00" * 4096;
    n = __jac_win_executable_path(buf, 4096);
    if n <= 0 {
        return "";
    }
    return buf[0:n].decode();
}
