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

obj Atom {}

obj Slot {
    has ref: (Atom | None) = None;
}

def names(slots: list[Slot], out: dict[str, int]) {
    for s in slots {
        name = s.ref?.missing;
        if not name {
            continue;
        }
        out[name] = 1;
    }
}

obj Settings {
    has files: (list[str] | None) = None;

    def load {
        self.files = ["a"];
    }
}

def reload(c: Settings) {
    assert c.files is None;
    c.load();
    assert c.files is not None;
    assert "a" in c.files;
}
