#Jac sets introduction
with entry {
    fruits = {"apple", "banana", "cherry"};
    print(fruits);
}

#Jac access set items

with entry {
    fruits = {"apple", "banana", "cherry"};
    for x in fruits {
        print(x);
    }
}

with entry {
    fruits = {"apple", "banana", "cherry"};
    print("banana" in fruits);
}

#Jac add set items

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

#Jac remove items

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

#Jac loop sets

with entry {
    fruits = {"apple", "banana", "cherry"};
    for x in fruits {
        print(x);
    }
}

#Jac join sets

with entry {
    set1 = {"a", "b", "c"};
    set2 = {1, 2, 3};

    set3 = set1.union(set2);
    print(set3);
}

with entry {
    set1 = {"a", "b", "c"};
    set2 = {1, 2, 3};

    set3 = set1 | set2;
    print(set3);
}

with entry {
    set1 = {"a", "b", "c"};
    set2 = {1, 2, 3};
    set3 = {"John", "Elena"};
    set4 = {"apple", "bananas", "cherry"};

    myset = set1.union(set2, set3, set4);
    print(myset);
}

with entry {
    set1 = {"a", "b", "c"};
    set2 = {1, 2, 3};
    set3 = {"John", "Elena"};
    set4 = {"apple", "bananas", "cherry"};

    myset = set1 | set2 | set3 | set4;
    print(myset);
}

with entry {
    set1 = {"a", "b", "c"};
    set2 = {1, 2, 3};

    set1.update(set2);
    print(set1);
}

with entry {
    set1 = {"apple", "banana", "cherry"};
    set2 = {"google", "microsoft", "apple"};

    set3 = set1.intersection(set2);
    print(set3);
}

with entry {
    set1 = {"apple", "banana", "cherry"};
    set2 = {"google", "microsoft", "apple"};

    set3 = set1 & set2;
    print(set3);
}

with entry {
    set1 = {"apple", "banana", "cherry"};
    set2 = {"google", "microsoft", "apple"};

    set3 = set1.difference(set2);

    print(set3);
}

with entry {
    set1 = {"apple", "banana", "cherry"};
    set2 = {"google", "microsoft", "apple"};

    set3 = set1 - set2;

    print(set3);
}
