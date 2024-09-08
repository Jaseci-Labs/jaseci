obj Animal {
    has :priv species: str;
    can :priv introduce() -> str {
        return "Hello, I am " + self.species + ". ";
    }
}

obj Dog: Animal: {
    has breed: str;
    can init(breed: str)-> None{
        super.init("Dog");
    }

    can :pub bark() -> str{
        return "Woof! Woof!";
    }
        obj Body {
        has :pub s: str="22";
    }
}

glob :priv body:int = 2, m = "hi";
with entry {
    myDog  = Dog(breed= "Golden Retriever");
    print( " Name: " + myDog.species );
    print( " Breed: " + myDog.breed );
    print( myDog.introduce() );
    print( myDog.bark() );
    body = myDog.Body("33");
    account = BankAccount(3333);
}
