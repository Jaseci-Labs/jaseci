"""Super simple example of inheritance."""

obj Parent {
    can init() -> None {
        # Parent initialization
    }
    can speak() -> None {
        # Parent speaking
    }
}

obj Child:Parent: {
    can init() -> None {
        # Child initialization
        Parent.init();  # Initialize parent, :o: is alias for :obj
    }
}