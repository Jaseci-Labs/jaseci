import:py from math, sin as s, cos, sqrt as sq;
include:py random;
import:py from ..test_cli, JacCliTests as Jac;

import:jac from deep.mycode, code as c;
import:jac hashcheck as h, assign_compr as a;
include:jac ignore;
import:jac from jacsamp, my_print as m;


with entry{
    print(sq(4), s(30),cos(30));
    print(randint(1, 10));
    print(m("--->my_print<---"));
    print(h.a, a.mvar);
    print(c());
    }