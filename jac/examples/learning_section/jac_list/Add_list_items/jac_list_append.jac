with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.append("orange");
    print(fruits);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    tropical = ["mango", "pineapple", "papaya"];
    fruits.extend(tropical);
    print(fruits);
}

with entry {
    fruits_list = ["apple", "banana", "cherry"];
    fruits_tuple = ("orange", "papaya");
    fruits_list.extend(fruits_tuple);
    print(fruits_list);
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    fruits.insert(1, "orange");
    print(fruits);
}
