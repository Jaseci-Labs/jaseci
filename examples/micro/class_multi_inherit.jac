"""Example of multiple inheritance."""

obj Parent {
    can init() -> None {
        # Parent initialization
    }
    can speak() -> None {
        # Parent speaking
    }
}

obj Mom:Parent: {
    can init() -> None {
        # Mom initialization
        Parent.init();
    }
    can speak() -> None {
        # Mom speaking
    }
}

obj Dad:Parent: {
    can init() -> None {
        # Dad initialization
        Parent.init();
    }
    can speak() -> None {
        # Dad speaking
    }
}

obj Child:Mom,Dad: { #Child inherits from Mom and Dad
    can init() -> None {
        # Child initialization
        Mom.init();
        Dad.init();
    }
}