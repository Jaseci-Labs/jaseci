"""Modified for separate defs/decls."""

object MyObj {
    has:prot a: int;
    can:priv init(a: int) -> None;
    can:pub set_a(val: int) -> None;
}

:o:MyObj:a:init {
        here.a = a;
}

:o:MyObj:a:set_a {
        here.a = val;
}