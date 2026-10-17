import from "libc.so.6" {
    def malloc(size: u64) -> ptr[u8];
    def free(p: ptr[u8]) -> None;
}

with entry {
    base: ptr[u32] = ptr[u32](malloc(64));
    p = base + 2;
    q = p - 1;
    d = p - base;
    i = int(base);
    r = ptr[u32](i + 4);
    print(d);
    print(int(p) - i);
    print(int(q) - i);
    print(int(r) - i);
    free(ptr[u8](i));
    print("done");
}
