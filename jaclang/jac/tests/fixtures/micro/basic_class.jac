"""Basic class implementation and spawning example."""

object Person {
    prot: has age: int;  # no need ot use `_age`
    pub: has name: str;

    priv: can init(name: str, age: int) -> None {
        here.name = name;
        here.age = age;
    }

    pub: can greet() -> None {  # public is default if `pub` is not specified
        print("Hello, my name is ", here.name, " and I'm ", here.age, " years old.");
    }
}

with entry {
    my_guy = Person("John", 42);
    my_guy.greet();
}