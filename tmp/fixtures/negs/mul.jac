import from "libc.so.6" {
    def malloc(size: u64) -> ptr[u8];
}
with entry {
    base: ptr[u32] = ptr[u32](malloc(64));
    d = base * 2;
    print(int(d));
}
