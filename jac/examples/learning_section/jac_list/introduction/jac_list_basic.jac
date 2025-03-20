with entry {
    fruits = ["apple", "banana", "cherry", "orange"];
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange", "cherry", "apple"];
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange"];
    print(len(fruits));
}

with entry {
    list1 = ["apple", "banana", "cherry"];
    list2 = [1, 5, 7, 9, 3];
    list3 = [True, False, False];
}

with entry {
    list1 = ["abc", 12, False, 40.25];
    print(list1);
}

with entry {
    fruits = list(("apple", "banana", "orange"));
    print(fruits);
}
