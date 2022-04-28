---
sidebar_position: 5
---

# Data Types

## Lists

- Lists are used to store multiple items in a single variable, meaning that any new items needs to be appended to the end of the list.
- List items are ordered, changeable, and allow duplicate values.
- List items are indexed, the first item has index [0], the second item has index [1] etc.
- List have the ability to store multi-typed data.
- List indices start at 0

```jac
// initializing an empty list
a = []

// initializing a list with data
a = [1, 2, 3, 4];

// modifying a specific index in a list
a[0] = [1,1];

// multi-dimensional lists access
a = [[0,0],[0,0]]
a[0][1] = 2; // this will result in [[0,2], [0,0]]

//sorting a list by a specific column
lst=[['b', 333],['c',245],['a', 56]];
std.sort_by_col(lst, 0);

//sorting a list by a specific column in reverse order
lst=[['b', 333],['c',245],['a', 56]];
std.sort_by_col(lst, 0, 'reverse');

// removing an item from a list
lst = ['a', 'b', 'c']
lst.destroy(1)  // removed b
```

## Dictionaries

- Dictionaries are used to store data values in key:value pairs.
- A dictionary is a collection which is changeable and does not allow duplicate keys.
- Dictionaries can store multi-type data

```jac
// initializing an empty dictionary
a = {}

// initializing a dictionary with data
a =  {"three": 3, "four": 4};

// accessing objects in a dictionary
a = {"one": {"inner": 44}, "two": 2};
std.out(a['one']); // prints {"inner": 44} to the console
```
