"""Test for base classes."""

import:jac from impl.imps, test_glob as mine;
include:jac impl.imps;

object Test {
    can init;
    can say_hi;
}

with enter {
    print(f"{mine}");
}