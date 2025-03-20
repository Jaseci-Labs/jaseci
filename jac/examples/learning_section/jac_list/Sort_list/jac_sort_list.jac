with entry {
    fruits = ["orange", "mango", "kiwi", "pineapple", "banana"];
    fruits.sort();
    print(fruits);
}

with entry {
    fruits = ["orange", "mango", "kiwi", "pineapple", "banana"];
    fruits.sort(reverse=True);
    print(fruits);
}

can myfunc(n: int) -> int {
    return abs(n - 50);
}

with entry {
    fruits = [100, 50, 65, 82, 23];
    fruits.sort(key=myfunc);
    print(fruits);
}

with entry {
    fruits = ["banana", "Orange", "Kiwi", "cherry"];
    fruits.sort();
    print(fruits);
}

with entry {
    fruits = ["banana", "Orange", "Kiwi", "cherry"];
    fruits.reverse();
    print(fruits);
}
