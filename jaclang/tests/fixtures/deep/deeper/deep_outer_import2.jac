import:jac from .., one_lev_dup;
import:jac from ..., needs_import_dup;

with entry {
    print(one_lev_dup.olprint());
    print(needs_import_dup.my_print(needs_import_dup.pyfunc));
}