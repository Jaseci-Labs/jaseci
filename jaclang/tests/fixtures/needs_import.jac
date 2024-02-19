"""Test of jac importing python."""

import:py pyfunc;
import:py random;
import:py from pyfunc, my_print;

with entry {
    my_print(pyfunc);
    print(random.random());
}
