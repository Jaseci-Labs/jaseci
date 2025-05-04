"""Minimal test file for type binding"""

obj Person {
    has name: str;
    has age: int;
    
    can greet {
        return "Hello";
    }
}

with entry {
    p = Person();
    p.greet();
}
