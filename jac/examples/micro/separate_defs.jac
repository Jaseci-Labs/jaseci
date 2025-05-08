"""Modified for separate defs/decls."""

obj MyObj {
    has : protect a: int;

    def : priv init(a: int) -> None;
    def : pub set_a(val: int) -> None;
}

impl def MyObj.init {
    here.a = a;
}

impl def MyObj.set_a {
    here.a = val;
}
