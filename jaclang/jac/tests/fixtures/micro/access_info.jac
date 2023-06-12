"""No more `_` and `__` for access/visibility directives."""

object MyObj {
    prot: has a: int;
    priv: can entry(a: int): None {
        here.a = a;
    }
    pub: can set_a(val: int): None {
        here.a = val;
    }
}