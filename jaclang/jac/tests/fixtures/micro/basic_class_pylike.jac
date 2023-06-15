"""A bit more chill approach."""

object Person {
    has age: int, name: str;

    can init(name: str, age: int) -> None {
        here.name = name;
        here.age = age;
    }

    can greet() -> None {
        print("Hello, my name is ", here.name, " and I'm ", here.age, " years old.");
    }
}

with entry {
    Person("John", 42).greet();
}