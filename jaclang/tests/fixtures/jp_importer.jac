import:py from math, sin as s, cos as c, sqrt as sq;
include:py random;

import:jac hashcheck as h;
include:jac ignore;
import:jac from jacsamp, my_print as m;


with entry{
    # print("math" in globals(),"---------------------");
    # print(math.sqrt(4));
    # print(random.randint(1, 10));
    print(sq(4), s(30));
    print(randint(1, 10));
    print(h.x);
    print(lllm);
    print(m("--->my_print<---"));

    }