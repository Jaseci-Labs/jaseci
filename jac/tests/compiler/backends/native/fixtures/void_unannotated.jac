"""Fixture for #7139: a callable written without `-> T` returns None.

The frontend types every one of these as returning `NoneType`, so native has
to lower them to `void` exactly like `-> None`: a function, a method, a
nested def, and an explicit `-> None` method whose call result used to be
replaced by an integer zero. Calling them as statements stays native.

`bump` is called from each of them so their side effects are observable.
"""

glob COUNTER: int = 0;

obj Box {
    has n: int = 0;

    def touch;
    def touch_twice -> None;
}

def bump {
    COUNTER += 1;
}

impl Box.touch {
    self.n += 1;
}

impl Box.touch_twice -> None {
    self.touch();
    self.touch();
    bump();
}

def free_fn {
    bump();
    return;
}

def outer -> int {
    def inner {
        bump();
    }
    inner();
    inner();
    return COUNTER;
}

def run -> int {
    COUNTER = 0;
    b = Box();
    b.touch();
    b.touch_twice();
    free_fn();
    return b.n * 100 + outer();
}

with entry {
    assert run() == 304;
    print("ok");
}
