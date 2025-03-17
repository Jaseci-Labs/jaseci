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