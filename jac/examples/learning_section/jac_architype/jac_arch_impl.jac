# Impls for Architypes
obj Person;

:obj:Person {
    can greet() {
        print("Hello!");
    }
}

# Impls for Abilities Inside Architypes
walker Animal {
    can eat(food: str);
}

:walker:Animal:can:eat(food: str) {
    print("Animal is eating " + food);
}