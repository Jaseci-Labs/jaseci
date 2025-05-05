import from ..one_lev_dup { olpyprint }
import from ...needs_import_dup { my_print, pyfunc }

with entry {
    # print(olpyprint());
    print(olprint());
    print(my_print(pyfunc));
}