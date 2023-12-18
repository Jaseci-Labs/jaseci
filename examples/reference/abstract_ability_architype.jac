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
