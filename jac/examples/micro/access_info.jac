"""No more `_` and `__` for access/visibility directives."""

obj MyObj {
    has : protect a: int;

    def : priv init(a: int) -> None {
        here.a = a;
    }

    def : pub set_a(val: int) -> None {
        here.a = val;
    }
}
