def tally(n: int) -> int {
    total = 0;
    add = lambda (t: int) -> int { total = total + t; return total; };
    for i in range(n) {
        add(i);
    }
    return total;
}

def outer(n: int) -> int {
    def inner(m: int) -> int {
        return m * 2;
    }
    return inner(n) + 1;
}

obj Point {
    has x: int = 0,
        y: int = 0;

    def norm1 -> int {
        return abs(self.x) + abs(self.y);
    }

    def shifted(dx: int) -> Point {
        return Point(x=self.x + dx, y=self.y);
    }

    static def origin -> Point {
        return Point();
    }
}

with entry {
    print(tally(4), outer(3), Point(x=1, y=-2).shifted(2).norm1(), Point.origin().x);
}
