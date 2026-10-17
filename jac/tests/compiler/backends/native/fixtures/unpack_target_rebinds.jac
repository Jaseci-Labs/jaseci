"""Loop targets unpacked from tuples that rebind a name to another type."""

def rebound -> list[float] {
    total = 0.0;
    names = 0;
    for (name, side) in [("a", 1.0), ("bb", -2.5)] {
        total += side;
        names += len(name);
    }
    for (side, sign) in [("l", 1.0), ("rr", -1.0)] {
        total += sign * float(len(side));
    }
    return [total, float(names)];
}

def kept -> int {
    total = 0;
    for (a, b) in [(1, 2), (3, 4)] {
        total += a * b;
    }
    for (a, b) in [(5, 6)] {
        total += a + b;
    }
    return total;
}

def swapped -> float {
    total = 0.0;
    for (k, v) in [(1, 2.0), (2, 3.0)] {
        total += float(k) * v;
    }
    for (v, k) in [(3.5, "zzz")] {
        total += v * float(len(k));
    }
    return total;
}

with entry {
    print(rebound());
    print(kept());
    print(swapped());
}
