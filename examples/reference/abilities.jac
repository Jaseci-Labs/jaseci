#Ability with decorators, access_modifiers
"""Calculator object with static method"""
obj Calculator{
    #static ability(function)

    static can :priv multiply(a :float, b :float) -> float{
        return a*b;
    }
}
with entry{
    print(Calculator.multiply(9,-2));
}
# Animal Archetype with an abstract ability
obj Animal {
    """Abstract ability for making a sound."""
    can make_sound -> str abs;
}

# Concrete obj representing a Dog
obj Dog:Animal: {
    """Overridden method to make a dog sound."""
    can make_sound -> str {
        return "Woof! Woof!";
    }
}

# Concrete obj representing a Cat
obj Cat:Animal: {
    """Overridden method to make a cat sound."""
    can make_sound -> str {
        return "Meow!";
    }
}

# Ability to simulate interactions with animals
can interact_with_animal(animal: Animal) -> None {
    sound = animal.make_sound();
    print(f"The animal says: {sound}");
}

# Usage
with entry{
    # Creating instances of concrete architypes
    Milo = Dog();
    Leo = Cat();

    # Interacting with animals
    interact_with_animal(Milo);
    interact_with_animal(Leo);
}
# Declaration
can greet(name: str) -> str;

# Definition after greet has been declared
:can:greet
(name: str) -> str {
    print(f"Hey, {name} Welcome to Jaseci!");

}
with entry{
    #ability calling
    greet('Coder');

}
#Simple Ability
"""Ability(Function) to calculate the numbers"""
can add(*a :tuple) -> int {
    return sum(a);
}

with entry{
    #ability calling
     print(add(9,-3,4));

}

