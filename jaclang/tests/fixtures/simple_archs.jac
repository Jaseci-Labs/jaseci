"""A Ninja Myca"""

obj SimpleObj {
    has var1: int,
        var2: int,
        var3: int = 0;
    can <post_init> {
       print(<s>.var1, <s>.var2, <s>.var3);
    }
}

class SimpleClass {
    has var1: int,
        var2: int,
        var3: int = 0;
    can <init> {
       print(<s>.var3);
    }
}

with entry {
    SimpleObj(1,2);
    SimpleClass();
}