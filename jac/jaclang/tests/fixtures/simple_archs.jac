"""A Ninja Myca"""

obj SimpleObj {
    has var1: int,
        var2: int,
        var3: int = 0;

    can postinit {
        print(self.var1, self.var2, self.var3);
    }
}

class SimpleClass {
    has var1: int,
        var2: int,
        var3: int = 0;

    can init(self: SimpleClass) {
        print(self.var3);
    }
}

with entry {
    SimpleObj(1, 2);
    SimpleClass();
}
