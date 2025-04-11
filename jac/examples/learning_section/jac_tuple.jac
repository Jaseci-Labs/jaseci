#introduction
with entry {
    fruits = ("apple", "banana", "cherry");
    print(fruits);
}

with entry {
    fruits = ("apple", "banana", "cherry", "apple", "cherry");
    print(fruits);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    print(len(fruits));
}

#Access tuple items

with entry {
    fruits = ("apple", "banana", "cherry");
    print(fruits[1]);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    print(fruits[-1]);
}

with entry {
    fruits = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango");
    print(fruits[2:5]);
}

with entry {
    fruits = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango");
    print(fruits[2:]);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    if "apple" in fruits {
        print("Yes, 'apple' is in the fruits tuple");
    }
}

#Update Tuple Items

with entry {
    x = ("apple", "banana", "cherry");
    y = list(x);
    y[1] = "kiwi";
    x = tuple(y);

    print(x);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    y = list(fruits);
    y.append("orange");
    fruits = tuple(y);
}

with entry {
    thistuple = ("apple", "banana", "cherry");
    y = ("orange", );
    thistuple += y;
    print(thistuple);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    y = list(fruits);
    y.remove("apple");
    fruits = tuple(y);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    del fruits;
}

#Unpack Tuple Items

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

#Loop Tuples

with entry {
    fruits = ("apple", "banana", "cherry");
    for x in fruits {
        print(x);
    }
}

with entry {
    fruits = ("apple", "banana", "cherry");
    for i in range(len(fruits)) {
        print(fruits[i]);
    }
}

with entry {
    fruits = ("apple", "banana", "cherry");
    i = 0;
    while i < len(fruits) {
        print(fruits[i]);
        i = i + 1;
    }
}

#Join Tuples

with entry {
    tuple1 = ("a", "b", "c");
    tuple2 = (1, 2, 3);

    tuple3 = tuple1 + tuple2;
    print(tuple3);
}

with entry {
    fruits = ("apple", "banana", "cherry");
    mytuple = fruits * 2;

    print(mytuple);
}
