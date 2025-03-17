obj Person {
    has name: str;

    can greet() {
        print("Hello!, my name is", self.name);
    }
}

with entry {
    person = Person("John");
    print("Name", person.name);
    person.greet();
}