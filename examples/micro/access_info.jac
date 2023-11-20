"""No more `_` and `__` for access/visibility directives."""

obj MyObj {
    has:protect a: int;
    can:priv init(a: int) -> None {
        <h>.a = a;
    }
    can:pub set_a(val: int) -> None {
        <h>.a = val;
    }
}