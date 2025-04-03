can say_hello {
    print("Hello!");
}

can say_hello_to(name: str) {
    print("Hello, " + name + "!");
}

can add(a: int, b: int) -> int {
    return a + b;
}

obj Maths {
    static can square(n: int) -> int {
        return n * n;
    }
}

can "subtract a and b" subtract(a: int, b: int) -> int {
    return a - b;
}

# Impls for Abilities
can say_bye(name: str);

:can:say_bye(name: str) {
    print("Bye, " + name + "!");
}

# Calling Abilities
with entry {
    say_hello();
}

with entry {
    say_hello_to("Alice");
}

# *args and *kwargs
can sum_all(*args: list) -> int {
    return sum(args);
}

with entry {
    print(sum_all(1, 2, 3, 4, 5));
}

can print_details(**kwargs: dict) {
    print(kwargs);
}

with entry {
    print_details(name="Alice", age="25");
}


# Recursion in Jac
# Factorial
can factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}

with entry {
    print(factorial(5));  # Output: 120
}

# Recursive Sum of a List
can recursive_sum(lst: list) -> int {
    if len(lst) == 1 {
        return lst[0];
    }
    return lst[0] + recursive_sum(lst[1:]);
}

with entry {
    print(recursive_sum([1, 2, 3, 4, 5]));  # Output: 15
}