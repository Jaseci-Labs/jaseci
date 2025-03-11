with entry {
    size = ["small", "medium", "large"];
    fruits = ["apple", "banana", "cherry"];
    for x in size {
        for y in fruits {
            print(x, y);
        }
    }
}
