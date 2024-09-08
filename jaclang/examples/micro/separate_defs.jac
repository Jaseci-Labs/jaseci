"""Modified for separate defs/decls."""

obj MyObj {
    has : protect a: int;

    can : priv init(a: int) -> None;
    can : pub set_a(val: int) -> None;
}

:o:MyObj:c:init {
    here.a = a;
}

:o:MyObj:c:set_a {
    here.a = val;
}
