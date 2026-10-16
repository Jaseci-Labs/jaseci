def lookup(t: (type | int), table: dict[type, str]) -> str {
    if isinstance(t, type) {
        if t is None {
            print(t.__name__);
        }
        return table[t];
    }
    return "";
}

def unreachable_attr(t: str) -> int {
    if not isinstance(t, str) {
        return t.bogus();
    }
    return len(t);
}

def still_typed {
    bad: int = "x";
}
