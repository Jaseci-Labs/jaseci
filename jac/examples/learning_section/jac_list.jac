#Introduction
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

#Access List Items

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

#Change List Items

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

#Add List Items

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

#Remove List Items

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

#Loop List Items

with entry {
    fruits = ["apple", "banana", "cherry"];
    for x in fruits {
        print(x);
    }
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    for i in range(len(fruits)) {
        print(fruits[i]);
    }
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    i = 0;
    while i < len(fruits) {
        print(fruits[i]);
        i = i + 1;
    }
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    [print(x) for x in fruits];
}

#Sort List

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

#Copy List

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

#Join List

with entry {
    list1 = ["a", "b", "c"];
    list2 = [1, 2, 3];

    list3 = list1 + list2;
    print(list3);
}

with entry {
    list1 = ["a", "b", "c"];
    list2 = [1, 2, 3];

    list1.extend(list2);
    print(list1);
}
