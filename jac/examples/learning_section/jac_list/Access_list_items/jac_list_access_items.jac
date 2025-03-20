with entry {
    fruits = ["apple", "banana", "cherry"];
    print(fruits[1]);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    print(fruits[-1]);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"];
    print(fruits[2:5]);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"];
    print(fruits[:4]);
}

with entry {
    fruits = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"];
    print(fruits[2:]);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    if "apple" in fruits {
        print("Yes, 'apple' is in the fruits list");
    }
}
