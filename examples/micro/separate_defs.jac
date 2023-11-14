"""Modified for separate defs/decls."""

obj MyObj {
    has:protected a: int;
    can:private init(a: int) -> None;
    can:public set_a(val: int) -> None;
}

:o:MyObj:a:init {
        <h>.a = a;
}

:o:MyObj:a:set_a {
        <h>.a = val;
}