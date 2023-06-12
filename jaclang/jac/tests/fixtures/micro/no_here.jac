"""Not focusing on the self is cleaner."""

object MyObj {
    has a: int;

    can entry(a: int): None {
        here.a = a;
    }

    can set_a(val: int): None {
        here.a = val;
    }
}