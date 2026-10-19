"""`flow f(func=x)`: a keyword argument named like `thread_run`'s own callable parameter still reaches `f`."""
def pick(func: int) -> int {
    return func;
}

with entry {
    by_keyword = flow pick(func=7) ;
    by_unpacking = flow pick(**{"func": 3}) ;
    print(f"keyword={wait by_keyword } unpacked={wait by_unpacking }");
}
