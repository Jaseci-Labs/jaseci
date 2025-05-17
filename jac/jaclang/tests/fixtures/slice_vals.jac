obj MyObj {
    has a: Annotated[Str, INT, BLAH] = "a";
    def foo(edge_spec: tuple[int, Optional[type], Optional[tuple]]) -> Architype;
}

impl MyObj.foo
(edge_spec: tuple[int, Optional[type], Optional[tuple]]) -> Architype {}