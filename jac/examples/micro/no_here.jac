"""Not focusing on the self is cleaner."""

obj MyObj {
    has a: int;

    can init(a: int) -> None {
        here.a = a;
    }

    can set_a(val: int) -> None {
        here.a = val;
    }
}
