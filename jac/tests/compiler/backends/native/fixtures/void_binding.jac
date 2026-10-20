"""Fixture: a void-typed call result used as a value.

Every callee here returns None, so it lowers to native `void` and its call
result has no storage: `-> None` and a missing `-> T` alike (#7139), for a
function, a method, and a nested def. Each `*_caller` uses that result as a
value, which the native backend must refuse with E5092 in the caller (so the
caller runs on the server and sees `None`), not crash in `_entry_alloca` on a
void pointee and not invent an integer zero the server would never produce.
"""

obj Sink {
    def annotated -> None {
        return;
    }

    def bare {}
}

def sink(x: int) -> None {
    return;
}

def bare_sink(x: int) {}

def caller(x: int) -> int {
    y = sink(x);
    return x;
}

def bare_caller(x: int) -> int {
    y = bare_sink(x);
    return x;
}

def method_caller(s: Sink) -> int {
    y = s.annotated();
    return 1;
}

def bare_method_caller(s: Sink) -> int {
    y = s.bare();
    return 1;
}

def nested_caller -> int {
    def inner {}
    y = inner();
    return 1;
}

def str_caller(x: int) -> str {
    return str(bare_sink(x));
}
