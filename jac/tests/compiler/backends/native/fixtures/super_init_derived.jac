"""`super.init(...)` reaching the initializer an `obj` derives from its fields."""

enum Kind { A = "a", B = "b" }

obj Tag {
    has label: str;
}

obj Shape {
    has kind: Kind;

    def area -> float abst;
}

obj Square(Shape) {
    has side: float;

    def init(side: float) {
        self.side = side;
        super.init(Kind.A);
    }

    override def area -> float {
        return self.side * self.side;
    }
}

obj Base {
    has kind: Kind;
    has name: str;
    has tags: list[str];
    has tag: Tag;
}

obj Mid(Base) {}

obj Leaf(Mid) {
    has extra: int;

    def init(extra: int, nm: str) {
        super.init(Kind.B, name=nm + "!", tags=["x", nm], tag=Tag(label=nm));
        self.extra = extra;
    }
}

with entry {
    sq = Square(3.0);
    print(sq.kind.value, sq.side, sq.area());
    for i in range(3) {
        leaf = Leaf(i, f"n{i}");
        print(leaf.extra, leaf.kind.value, leaf.name, leaf.tags, leaf.tag.label);
    }
}
