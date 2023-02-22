# Jaseci Dictionary Methods

In this section, the table below displays all of the **list** methods available in Jaseci for manipulating lists. These methods provide a comprehensive and efficient way to work with lists in your application.

| Op         | Args | Description                            |
| ---------- | ---- | -------------------------------------- |
| .list::max | none | Returns the maximum value of the list. |

**Example Usage**

```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::max;
}
```

**Expected Output**
```
"report": [
    78
  ]
```


| Op         | Args | Description                            |
| ---------- | ---- | -------------------------------------- |
| .list::min | none | Returns the minimum value of the list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::min;
}
```

**Expected Output**
```
"report": [
    3
  ]
```

| Op                | Args | Description                                         |
| ----------------- | ---- | --------------------------------------------------- |
| .list::idx_of_max | none | Returns the index of the maximum value of the list. |

**Example Usage**

```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::min;
}
```

**Expected Output**

```
"report": [
    8
  ]
```

| Op                | Args | Description                                         |
| ----------------- | ---- | --------------------------------------------------- |
| .list::idx_of_min | none | Returns the index of the minimum value of the list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::idx_of_min;
}
```

**Expected Output**
```
 "report": [
    3
  ]
```


| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .list::copy | none | Returns a shallow copy of the list |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::copy;
}
```
**Expected Output**
```
 "report": [
    [23,45,12,3,44,67,23,12,78]
  ],
```

| Op              | Args | Description                     |
| --------------- | ---- | ------------------------------- |
| .list::deepcopy | none | Returns a deep copy of the list |

**Example Usage**

```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::deepcopy;
}
```

**Expected Output**
```
 "report": [
    [23,45,12,3,44,67,23,12,78]
  ]
```

| Op          | Args | Description                                    |
| ----------- | ---- | ---------------------------------------------- |
| .list::sort | none | Sort the values in the list in assending order |

**Example Usage**

```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::sort;
    report _list;
}
```

**Expected Output**

```
"report": [
    [3,12,12,23,23,44,45,67,78]
  ]
```

| Op             | Args | Description                    |
| -------------- | ---- | ------------------------------ |
| .list::reverse | none | Reverse the items in the list. |

**Example Usage**

```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::reverse;
    report _list;
}
```

**Expected Output**
```
"report": [
    [78,12,23,67,44,3,12,45,23]
  ]
```

| Op           | Args | Description                      |
| ------------ | ---- | -------------------------------- |
| .list::clear | none | Clear all the values in the list |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::clear;
    report _list;
}
```

**Expected Output**
```
 "report": [
    []
  ]
```

| Op         | Args     | Description                       |
| ---------- | -------- | --------------------------------- |
| .list::pop | optional | Pops the last item from the list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::pop;
    report _list;
}
```
**Expected Output**
```
"report": [
    [23,45,12,3,44,67,23,12]
  ],
```

| Op           | Args            | Description                           |
| ------------ | --------------- | ------------------------------------- |
| .list::index | value from list | Returns the index of the given value. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::index(44);
}
```

**Expected Output**
```
"report": [
    4
  ],
```

| Op            | Args        | Description                             |
| ------------- | ----------- | --------------------------------------- |
| .list::append | a new value | Append an new value in the end of list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::append(56);
    report _list;
}
```

**Expected Output**
```
"report": [
    [23,45,12,3,44,67,23,12,78,56]
  ]
```

| Op            | Args           | Description                                            |
| ------------- | -------------- | ------------------------------------------------------ |
| .list::extend | list of values | Concat list of values to the end of the existing list. |


**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::extend([56,34,72]);
    report _list;
}
```

**Expected Output**
```
"report": [
    [23,45,12,3,44,67,23,12,78,56,34,72]
  ]
```

| Op            | Args        | Description                                        |
| ------------- | ----------- | -------------------------------------------------- |
| .list::insert | index,value | Insert given value at the given index of the list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::insert(2,34);
    report _list;
}
```


**Expected Output**
```
"report": [
    [23,45,34,12,3,44,67,23,12,78]
  ]
```

| Op            | Args  | Description                                                                                                       |
| ------------- | ----- | ----------------------------------------------------------------------------------------------------------------- |
| .list::remove | value | Remove the given value from the list. (If there are duplicates of the same value this removes only the first one) |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::remove(12);
    report _list;
}
```
**Expected Output**
```
  "report": [
    [23,45,3,44,67,23,12,78]
  ]
```

| Op           | Args  | Description                                          |
| ------------ | ----- | ---------------------------------------------------- |
| .list::count | value | Returns the number of occurences of the given value. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::count(12);
}
```
**Expected Output**
```
 "report": [
    2
  ]
```

| Op              | Args | Description                                              |
| --------------- | ---- | -------------------------------------------------------- |
| .list::pairwise | none | Return successive overlapping pairs taken from the list. |

**Example Usage**
```
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::pairwise;
}
```
**Expected Output**
```
"report": [
    [
      [23,45],
      [45,12],
      [12,3],
      [3,44],
      [44,67],
      [67,23],
      [23,12],
      [12,78]
    ]
  ],
```