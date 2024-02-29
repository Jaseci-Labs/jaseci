"""Super simple example of inheritance."""

obj Parent {
    can init {
    # Parent initialization
    }

    can speak() -> None {
    # Parent speaking
    }
}

obj Child :Parent: {
    can init {
    # Child initialization
    Parent.init(); # Initialize parent, :o: is alias for :obj
    }
}
