import from "libc.so.6" {
    def malloc(size: u64) -> ptr[u8];
    def free(p: ptr[u8]) -> None;
}
import from c {
    obj Pair {
        has a: i64,
            b: f64;
    }
}

with entry {
    base: ptr[Pair] = ptr[Pair](malloc(64));
    base.a = 41;
    base.a += 1;
    base.b = 2.5;
    p = base + 1;
    p.a = 7;
    d = p - base;
    print(base.a);
    print(base.b);
    print(p.a);
    print(d);
    free(ptr[u8](int(base)));
}
