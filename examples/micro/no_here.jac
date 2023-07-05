"""Not focusing on the self is cleaner."""

object MyObj {
    has a: int;

    can init(a: int) -> None {
        <h>.a = a;
    }

    can set_a(val: int) -> None {
        <h>.a = val;
    }
}