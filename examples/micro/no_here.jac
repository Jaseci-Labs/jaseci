"""Not focusing on the self is cleaner."""

obj MyObj {
    has a: int;

    can init(a: int) -> None {
        <h>.a = a;
    }

    can set_a(val: int) -> None {
        <h>.a = val;
    }
}