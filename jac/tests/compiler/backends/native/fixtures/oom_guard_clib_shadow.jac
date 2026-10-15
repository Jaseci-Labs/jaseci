"""The module shadows libc's `write` with a user-facing signature whose ABI is
incompatible with the POSIX one (i32 return, an i64 buffer, i32 count). The
malloc-NULL guard in the RC allocators also reaches for `write`, and
`_get_or_declare_extern` rightly refuses to adapt that declaration -- the
guard must still emit its trap instead of failing the compile. Only compiled
to IR, never run."""

import from "libc.so.6" { def write(fd: i32, buf: int, count: i32) -> i32;  }

glob items: list[int] = [];

def push(x: int) -> int {
    items.append(x);
    return len(items);
}
