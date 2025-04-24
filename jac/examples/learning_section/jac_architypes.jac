# These Architypes has been declared without a body
class Home {}

obj Car {}

node Person {}

edge Friendship {}

walker Greeting {}


# semstring of Architype
obj "A vehicle for transportation" Vehicle {
    has model: str;
    has color: str;
}


# creating an object of Architype
obj MyObject {
    has x: int = 2;
}

with entry {
    object1 = MyObject();
    print(object1.x);
}


# ------------------------------------------- #
# Attribute in Architype
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

# ------------------------------------------- #
# Abilities in Architype
class Home {
    can live() {
        print("You are now home!");
    }
}

obj Car {
    can drive() {
        print("Vroom vroom!");
    }
}

node Person {
    can greet() {
        print("Hello!");
    }
}

edge Friendship {
    can be_friend() {
        print("You are now friends!");
    }
}


# Override function in subclass
obj Animal {
    can speak {
        print("Some sound...");
    }
}

obj Dog: Animal: {
    override can speak {
        print("Woof! Woof!");
    }
}

# Abstract Abilities
obj Shape {
    can draw abs;
}

obj Circle: Shape: {
    override can draw {
        print("Drawing a circle...");
    }
}


# ------------------------------------------- #
# Inheritence in Architype
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


# ------------------------------------------- #
# Impls in Architype
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