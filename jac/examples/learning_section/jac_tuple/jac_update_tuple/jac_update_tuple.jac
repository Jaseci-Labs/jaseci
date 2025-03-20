with entry {
    x = ("apple", "banana", "cherry");
    y = list(x);
    y[1] = "kiwi";
    x = tuple(y);

    print(x);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    y = list(fruits);
    y.append("orange");
    fruits = tuple(y);
}

with entry {
    thistuple = ("apple", "banana", "cherry");
    y = ("orange", );
    thistuple += y;
    print(thistuple);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    y = list(fruits);
    y.remove("apple");
    fruits = tuple(y);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    del fruits;
}
