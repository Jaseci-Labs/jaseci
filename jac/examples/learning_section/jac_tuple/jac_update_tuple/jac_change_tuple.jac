with entry {
    x = ("apple", "banana", "cherry");
    y = list(x);
    y[1] = "kiwi";
    x = tuple(y);

    print(x);
}
