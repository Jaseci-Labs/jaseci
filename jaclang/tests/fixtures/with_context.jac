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
}
