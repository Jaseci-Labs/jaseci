"""Super simple example of inheritance."""

object Parent {
    can init() -> None {
        # Parent initialization
    }
    can speak() -> None {
        # Parent speaking
    }
}

object Child:Parent {
    can init() -> None {
        # Child initialization
        Parent.init();  # Initialize parent, :o: is alias for :object:
    }
}