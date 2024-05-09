# import:py from ..one_lev_dup_py, olpyprint;
import:jac from ..one_lev_dup, olprint;
import:jac from ...needs_import_dup, my_print, pyfunc;

with entry {
    # print(olpyprint());
    print(olprint());
    print(my_print(pyfunc));
}