
# 1. Test initialization order.
obj Test1 {
    has var1: int;
    has var2: int = 42;
    has var3: int; # <-- This should be syntax error.
}

# 2. Test if all un initialized vars are initialized in the init method.
obj Test2 {
    has var1: int;
    has var2: int;
    has var3: int;
    has var4: int = 42;

    can init() {  # <-- Should be error because "var2", "var3" are not initialized.
        self.var1 = 1;
    }
}

# 3. Test the same of Test2 but the init is defined somewhere else.
obj Test3 {
    has var1: int;
    has var2: int;
    has var3: int;
    has var4: int = 42;

    can init();
}

:obj:Test3:can:init() {
    self.var1 = 1;
}

# 4. Test if postinit is needed but not provided.
obj Test4 {
    has var1: str;
    has var2: int by postinit;
}

# 5. Test if a postinit var is not initialized by postinit method.
obj Test5 {
    has var1: str;
    has var2: int by postinit;

    can postinit() {
    }
}

# 6. Postinit should be considered as has default initialization.
obj Test1 {
    has var1: int;
    has var2: int = 42;
    has var3: int by postinit;  # <-- This is fine.
    has var4: int;  # <-- This should be syntax error.

    can postinit() {
        self.var3 = 3;
    }
}

