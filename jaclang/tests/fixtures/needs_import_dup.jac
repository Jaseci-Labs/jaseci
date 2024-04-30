"""Test of jac importing python."""
import:py os;
import:py pyfunc;
import:py random;
import:py from pyfunc, my_print;

with entry {

    my_print(pyfunc);
    print(random.random());
}

import:py circle_pysolo;
import:py from circle_pysolo, calculate_area;

with entry {
    print(f"are {calculate_area(2.0)}");
}
