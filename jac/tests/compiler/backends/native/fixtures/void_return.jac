"""Fixture for #8085: an explicit `return` inside a `-> None` callable.

`-> None` lowers to an LLVM function returning `void`, and so does a callable
with no `-> T` at all (#7139), so every one of these has to end in
`ret void`. A `return <expr>` that lowered as `ret <expr>` produced a
value-returning terminator inside a void function, which LLVM refuses to
parse -- taking the whole module's codegen with it.

`bump` is called from each of them so the side effect is observable: a return
still has to evaluate its expression before discarding the value.
"""

glob COUNTER: int = 0;

obj Box {
    has n: int = 0;

    def touch -> None;
    def touch_call -> None;
    def bare_touch;
}

def bump {
    COUNTER += 1;
}

impl Box.touch -> None {
    self.n += 1;
    return None;
}

impl Box.touch_call -> None {
    return bump();
}

impl Box.bare_touch {
    self.n += 1;
}

def free_fn -> None {
    return None;
}

def bare_fn {
    bump();
}

def outer {
    def inner {
        bump();
    }
    inner();
}

def run -> int {
    COUNTER = 0;
    b = Box();
    b.touch();
    b.touch();
    b.touch_call();
    b.bare_touch();
    free_fn();
    bare_fn();
    outer();
    return b.n * 100 + COUNTER;
}

with entry {
    assert run() == 303;
    print("ok");
}
