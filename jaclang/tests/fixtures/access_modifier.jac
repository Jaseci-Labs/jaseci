obj Animal {
    has :pub species: str;

    can :priv introduce() {
        return "Hello, I am " + self.species + ". ";
    }


}

obj Dog: Animal: {
    has :pub breed: str;

    can init(breed: str) {
        super.init("Dog");
        self.breed = breed;
    }

    can :pub bark() {
        return "Woof! Woof!";
    }

    can :pub makeSound() {
        return "The dog says: " + super.introduce();
    }
        obj Body {
        has :pub s: str="22";
    }
}

with entry {
     myDog = Dog(breed= "Golden Retriever");

    print( " Name: " + myDog.species );
    print( " Breed: " + myDog.breed );
    print( myDog.introduce() );
    print( myDog.bark() );
    b=myDog.Body("33");
    x=b.s;
    print(x);
}
