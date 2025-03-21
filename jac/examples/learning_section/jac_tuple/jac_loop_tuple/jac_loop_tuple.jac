with entry {
    fruits = ("apple", "banana", "cherry");
    for x in fruits {
        print(x);
    }
}

with entry {
    fruits = ("apple", "banana", "cherry");
    for i in range(len(fruits)) {
        print(fruits[i]);
    }
}

with entry {
    fruits = ("apple", "banana", "cherry");
    i = 0;
    while i < len(fruits) {
        print(fruits[i]);
        i = i + 1;
    }
}
