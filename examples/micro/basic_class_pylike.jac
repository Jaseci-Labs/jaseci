"""A bit more chill approach."""

object Person {
    has age: int, name: str;

    can init(name: str, age: int) -> None {
        <h>.name = name;
        <h>.age = age;
    }

    can greet() -> None {
        print("Hello, my name is ", <h>.name, " and I'm ", <h>.age, " years old.");
    }
}

with enter {
    Person("John", 42).greet();
}