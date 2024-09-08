"""Example of multiple inheritance."""

obj Parent {
    can init {
    # Parent initialization
    }
    can speak() -> None abs;# Abstract method
}

obj Mom :Parent: {
    can init {
    # Mom initialization
    Parent.init();
    }

    can speak() -> None {
        print("I'm good at swimming!");
    }
}

obj Dad :Parent: {
    can init {
    # Dad initialization
    Parent.init();
    }

    can speak() -> None {
        print("I'm good at running!");
    }
}

obj Child :Mom, Dad: { #Child inherits from Mom and Dad

can speak() -> None {
# Child initialization
Mom.speak();
Dad.speak();
}
}
