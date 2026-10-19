import from "libcef.so" {
    def cef_version_info(which: i32) -> i32;  obj cef_ptr_wrap_t {
        has p0: int = 0,
            p1: int = 0;
    }
}

import from "libc.so.6" {
    def calloc(n: int, size: int) -> int;  def free(ptr: int) -> None;  def memset(
        s: int, c: i32, n: int
    ) -> int;  def memcpy(dst: int, src: int, n: int) -> int;  def open(
        path: str, flags: i32
    ) -> i32;  def read(fd: i32, buf: int, count: int) -> int;  def close(
        fd: i32
    ) -> i32;  def strlen(s: str) -> int;  def write(
        fd: i32, buf: int, count: int
    ) -> int;  def abort -> None;
}
