with entry {
    fruits = {"apple", "banana", "cherry"};
    fruits.remove("banana");
    print(fruits);
}

with entry {
    fruits = {"apple", "banana", "cherry"};
    fruits.discard("banana");
    print(fruits);
}

with entry {
    fruits = {"apple", "banana", "cherry"};
    x = fruits.pop();
    print(x);
    print(fruits);
}

with entry {
    fruits = {"apple", "banana", "cherry"};
    fruits.clear();
    print(fruits);
}

with entry {
    fruits = {"apple", "banana", "cherry"};
    del fruits;
}
