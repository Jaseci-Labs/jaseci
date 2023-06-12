"""Modified for separate defs/decls."""

object MyObj {
    prot: has a: int;
    priv: can entry(a: int): None;
    pub: can set_a(val: int): None;
}

:o:MyObj:a:entry {
        here.a = a;
}

:o:MyObj:a:set_a {
        here.a = val;
}