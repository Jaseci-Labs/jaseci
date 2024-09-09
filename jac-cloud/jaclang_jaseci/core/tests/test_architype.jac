node a {
    has val: str;
}

with entry {
    print(a(val=1).__jac__.serialize());
}