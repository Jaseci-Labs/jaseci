"""No more `_` and `__` for access/visibility directives."""

object MyObj {
    has:prot a: int;
    can:priv init(a: int) -> None {
        here.a = a;
    }
    can:pub set_a(val: int) -> None {
        here.a = val;
    }
}