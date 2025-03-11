with entry{
    fruits = ["apple","banana","cherry","orange"];
    print(fruits);
}

"""Allow Duplicates"""
with entry{
    fruits = ["apple","banana","cherry","orange","cherry","apple"];
    print(fruits);
}

"""List Length"""
with entry{
    fruits = ["apple","banana","cherry","orange"];
    print(len(fruits));
}

"""List Items - Data Types"""
with entry{
    list1 = ["apple", "banana", "cherry"];
    list2 = [1, 5, 7, 9, 3];
    list3 = [True, False, False];
}

"""A list can contain different data types"""
with entry{
    list1 = ["abc",12, False,40.25];
    print(list1);
}

"""The list() Constructor"""
with entry{
    fruits = list(("apple","banana","orange"));
    print(fruits);
}