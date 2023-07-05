"""Basic class implementation and spawning example."""

object Person {
    has:prot age: int;  # no need ot use `_age`
    has:pub name: str;

    can:priv init(name: str, age: int) -> None {
        <h>.name = name;
        <h>.age = age;
    }

    can:pub greet() -> None {  # public is default if `pub` is not specified
        print("Hello, my name is ", <h>.name, " and I'm ", <h>.age, " years old.");
    }
}

with entry {
    my_guy = Person("John", 42);
    my_guy.greet();
}