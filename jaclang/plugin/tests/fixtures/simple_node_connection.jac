node simple {
    has tag: str;
}
with entry {
    root ++> simple(tag="first");
    root ++> simple(tag="second");
    print([root -->]);
}