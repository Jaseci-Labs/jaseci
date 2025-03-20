with entry {
    fruits = ("apple", "banana", "cherry");
    (green, yellow, red) = fruits;

    print(green);
    print(yellow);
    print(red);
}

with entry {
    fruits = ("apple", "banana", "cherry", "strawberry", "raspberry");
    (green, yellow, *red) = fruits;

    print(green);
    print(yellow);
    print(red);
}

with entry {
    fruits = ("apple", "mango", "papaya", "pineapple", "cherry");

    (green, *tropic, red) = fruits;

    print(green);
    print(tropic);
    print(red);
}
