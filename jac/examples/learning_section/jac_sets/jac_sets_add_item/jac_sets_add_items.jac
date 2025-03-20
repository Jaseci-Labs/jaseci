with entry {
    fruits = {"apple", "banana", "cherry"};
    fruits.add("orange");
    print(fruits);
}

with entry {
    fruits_1 = {"apple", "banana", "cherry"};
    fruits_2 = {"pineapple", "mango", "papaya"};

    fruits_1.update(fruits_2);

    print(fruits_1);
}

with entry {
    fruits_1 = {"apple", "banana", "cherry"};
    fruits_2 = ["kiwi", "orange"];

    fruits_1.update(fruits_2);

    print(fruits_1);
}
