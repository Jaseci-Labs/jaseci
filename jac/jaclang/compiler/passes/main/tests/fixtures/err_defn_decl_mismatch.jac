

obj SomeObj {
    can foo(param1: str, param2:int) -> str;
    can bar(param1: str, param2:int) -> str;
}


# Miss match parameter count.
:obj:SomeObj:can:foo(param1: str) -> str {
    return "foo";
}


# Mis matching parameter name.
:obj:SomeObj:can:bar(param1: str, praam2:int) -> str {
    return "bar";
}

