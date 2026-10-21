"""A raised value and a `from` cause must be exceptions (a cause may also be None).

`any`, `type[E]`, narrowed optionals and bounded TypeVars are accepted; a
non-exception, `None`, or a union with a non-exception member is E1090, and a
non-exception cause is E1161.
"""

obj NotAnError {}

def raise_any_subscript(b: dict[str, any]) {
    raise b["error"];
}

def raise_any_param(e: any) {
    raise e;
}

def raise_exception_class(t: type[ValueError]) {
    raise t;
}

def raise_exception_union(e: ValueError | TypeError) {
    raise e;
}

def raise_narrowed_optional(e: ValueError | None) {
    if e is not None {
        raise e;
    }
}

def raise_bounded_type_var[T: Exception](e: T) {
    raise e;
}

def raise_from_valid_causes(c: Exception | None, d: any) {
    raise ValueError("a") from c;
    raise ValueError("b") from d;
    raise ValueError("c") from None;
}

def raise_int {
    raise 5;
}

def raise_non_exception_instance {
    raise NotAnError();
}

def raise_optional(e: ValueError | None) {
    raise e;
}

def raise_mixed_union(e: ValueError | int) {
    raise e;
}

def raise_from_int {
    raise ValueError("x") from 5;
}
