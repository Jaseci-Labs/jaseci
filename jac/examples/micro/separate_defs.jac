"""Modified for separate defs/decls."""

obj MyObj {
    has : protect a: int;

    def : priv init(a: int) -> None;
    def : pub set_a(val: int) -> None;
}

:o:MyObj:c:init {
    here.a = a;
}

:o:MyObj:c:set_a {
    here.a = val;
}
