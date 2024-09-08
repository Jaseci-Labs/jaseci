"""No more `_` and `__` for access/visibility directives."""

obj MyObj {
    has:protect a: int;
    can:priv init(a: int) -> None {
        here.a = a;
    }
    can:pub set_a(val: int) -> None {
        here.a = val;;;;;
    }
}