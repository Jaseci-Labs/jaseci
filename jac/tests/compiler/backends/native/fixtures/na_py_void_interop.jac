"""Fixture for #7139: callables returning None across the native/Python bridge.

`native_note` (no `-> T`) and `native_ack` (`-> None`) are native and lower to
`void`; the Python stub that calls them must declare a `None` restype, or it
reads whatever the return register holds as an int. Both call back into
`py_note`, a Python function with no `-> T`, which the native side has to
declare `void` and whose ctypes callback must accept a `None` result.
"""

def py_note(x: int) {
    print(x);
}

def native_note(x: int) {
    py_note(x);
}

def native_ack(x: int) -> None {
    py_note(x + 1);
    return;
}

with entry {
    a = native_note(1);
    b = native_ack(2);
    print(a is None, b is None);
}
