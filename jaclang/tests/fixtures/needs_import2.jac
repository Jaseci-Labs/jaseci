"""Test of jac importing python."""
import:jac pyfunc;
import:jac from pyfunc, my_print;

with entry {
    my_print(X = pyfunc);
}

