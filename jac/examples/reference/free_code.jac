import math;

obj circle {
    can init(radius: float) {
        self.radius = radius;
    }

    can area -> float {
        return math.pi * self.radius * self.radius;
    }
}

can foo(n_1: float) {
    return n_1 ** 2;
}

with entry {
    print("Hello World!");
    print(foo(7));
    print(int(circle(10).area()));

    #code block
}
