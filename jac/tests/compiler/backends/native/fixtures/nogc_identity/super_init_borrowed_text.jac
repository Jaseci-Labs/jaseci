"""`super.init(...)` into the initializer an `obj` derives from its fields,
where a later argument reads a field an earlier one replaces. Every argument
is owned before any field changes, so `second` keeps the text `first` held
rather than memory the store into `first` freed."""

obj Named {
    has first: str,
        second: str;
}

obj NamedChild(Named) {
    def init(seed: &str) {
        self.first = seed + "-old";
        super.init(seed + "-new", self.first);
    }
}

def run -> int {
    total = 0;
    for i in range(40) {
        seed = f"seed{i}";
        nc = NamedChild(&seed);
        if i < 3 {
            print(nc.first, nc.second);
        }
        total += len(nc.first) + len(nc.second);
    }
    return total;
}

with entry {
    print(run());
}
