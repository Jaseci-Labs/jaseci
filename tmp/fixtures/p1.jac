import from "libc.so.6" { obj tiny { has x: i32 = 0; } }
glob T5: tiny = tiny(6);
def f() -> i32 {
    return T5.x;
}
with entry {
    print(f());
}
