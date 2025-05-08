"""Not focusing on the self is cleaner."""

obj MyObj {
    has a: int;

    def init(a: int) -> None {
        here.a = a;
    }

    def set_a(val: int) -> None {
        here.a = val;
    }
}
