with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.remove("apple");
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry", "banana", "kiwi"];
    fruits.remove("banana");
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.pop(1);
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.pop();
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    del fruits[0];
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    del fruits;
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.clear();
    print(fruits);
}
