"""No more `_` and `__` for access/visibility directives."""

object MyObj {
    has:protected a: int;
    can:private init(a: int) -> None {
        <h>.a = a;
    }
    can:public set_a(val: int) -> None {
        <h>.a = val;;;;;
    }
}