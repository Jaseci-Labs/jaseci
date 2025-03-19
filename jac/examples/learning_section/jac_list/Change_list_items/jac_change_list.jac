with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits[1] = "orange";
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange", "kiwi", "mango"];
    fruits[1:3] = ["blackcurrant", "watermelon"];
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.insert(2, "watermelon");
    print(fruits);
}
