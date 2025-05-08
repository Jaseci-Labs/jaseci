"""Basic class implementation and spawning example."""

obj Person {
    has : protect age: int; # no need ot use `_age`
    has : pub name: str;

    def : priv init(name: str, age: int) -> None {
        here.name = name;
        here.age = age;
    }

    def : pub greet() -> None { # public is default if `pub` is not specified

    print("Hello, my name is ", here.name, " and I'm ", here.age, " years old.");
    }
}

with entry {
    my_guy = Person("John", 42);
    my_guy.greet();
}
