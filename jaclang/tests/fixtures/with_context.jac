can init;

obj TestType {
    can __enter__ {
        print("im in");
    }

    can __exit__(exc_type: object, exc_value: object, traceback: object) {
        print("im out");
    }
}

with entry {
    x = TestType();
    with x {
        print("in the middle");
    }
    init();
}

:can:init {
    print("init");
}


with entry {
    x = ["apple", "banana", "cherry"];
    nums = [1, 2, 3, 4, 5, 6];
    print({fruit: nums[0:3] for (i, fruit) in enumerate(x)});
}