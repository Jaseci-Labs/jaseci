with entry {
    fruits = ["apple", "banana", "cherry"];
    mylist = fruits.copy();
    print(mylist);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    mylist = fruits[:];
    print(mylist);
}
