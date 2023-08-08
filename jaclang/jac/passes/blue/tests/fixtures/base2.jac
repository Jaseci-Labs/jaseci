"""Test for base classes."""

import:jac from impl.imps, test_glob as mine;

object Test {
    can init;
    can say_hi;
}

with entry {
    print(f"{mine}");
}

include:jac impl.imps;