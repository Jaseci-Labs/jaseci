import:jac from ..one_lev_dup, olprint;
import:jac from ...needs_import_dup, my_print, pyfunc;

with entry {
    print(olprint());
    print(my_print(pyfunc));
}