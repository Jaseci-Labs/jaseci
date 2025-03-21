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