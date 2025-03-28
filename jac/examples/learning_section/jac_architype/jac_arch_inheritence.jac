obj Animal {
    has color: int;
    can eat {
        print("Animal is eating");
    }
}

node Pet: Animal: {}

with entry {
    pet = Pet("Brown");
    pet.eat();
    print(pet.color);
}