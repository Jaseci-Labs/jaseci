"""Generic methods on archetypes monomorphize per call site (#7626 A4).

`Box.pick[T]` registers as a method template (keyed Arch.method) instead
of hitting the declaration-time unlowerable-type error; each call site
stamps a specialization with `self` prepended to the specialized
signature and dispatches it directly, including a call to itself from
inside its own specialization.
"""

obj Box {
    has val: int = 0;

    def pick[T](a: T, b: T) -> T {
        return a if self.val > 0 else b;
    }
}

def pick_int(v: int) -> int {
    return Box(val=v).pick(7, 9);
}

def pick_str_len(v: int) -> int {
    a: str = "xx";
    b: str = "yyy";
    return len(Box(val=v).pick(a, b));
}

obj Tree {
    has kids: list[Tree] = [];

    def count_of[T](typ: type[T]) -> int {
        n = 0;
        for k in self.kids {
            if isinstance(k, typ) {
                n += 1;
            }
            n += k.count_of(typ);
        }
        return n;
    }
}

obj Leaf(Tree) {}

obj Mid(Tree) {}

def count_leaves -> int {
    top = Mid(kids=[Leaf(), Mid(kids=[Leaf(), Leaf()])]);
    return top.count_of(Leaf);
}
