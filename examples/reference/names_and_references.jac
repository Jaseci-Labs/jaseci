obj Animal {
    can init(species: str) {
        self.species = species;
    }
}

obj Dog :Animal: {
    can init(breed: str) {
        super.init(species='Dog');
        self.breed = breed;
        self.sound = "";
        self.postinit();
    }
    can postinit;
}

:obj:Dog:can:postinit {
    self.sound = 'woof woof';
}

with entry {
    dog1 = Dog("Labrador");
    print(dog1.species, dog1.breed, dog1.sound);
}
