with entry {
    try  {
        print(x);
    } except NameError {
        print("An exception occurred");
    }
}

with entry {
    try  {
        print(x);
    } except NameError {
        print("Variable x is not defined");
    }else {
        print("Something else went wrong");
    }
}

with entry {
    try  {
        print(x);
    } except NameError {
        print("Variable x is not defined");
    } finally {
        print("Something else went wrong");
    }
}

can foo(value: int) {
    if value < 0 {
        raise ValueError("Value must be non-negative");
    }
}

with entry {
    try  {
        foo(-1);
    } except ValueError as e {
        print("Raised:", e);
    }
}
