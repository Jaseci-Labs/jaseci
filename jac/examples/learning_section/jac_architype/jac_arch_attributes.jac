class Home {
    has address: str;
}

obj Car {
    has color: str;
}

node Dog {
    has eyes: int = 2;
}

edge Friendship {
    has since: int;
}

walker Greeting {
    has message: str;
}


# Architype with inline attribute declaration
obj Person {
    has name: str;
    has age: int;
}

obj Car {
    has model: str, color: str, year: int;
}

# Static attribute in Architype
obj Van {
    static has wheels: int = 4;
}

with entry {
    print(Van.wheels);
}