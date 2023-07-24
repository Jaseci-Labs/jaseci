---
sidebar_position: 2
title: Lists
description: Methods available in Jaseci for manipulating lists.
---

# List

In this section you will find all of the list methods available in Jaseci for manipulating lists. These methods provide a comprehensive and efficient way to work with lists in your application.

### `max`

|             |                                        |
| ----------- | -------------------------------------- |
| Op          | .list::max                             |
| Args        | None                                   |
| Description | Returns the maximum value of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::max;
}
```

**Expected Output**

```json
"report": [
    78
  ]
```

### `min`

|             |                                        |
| ----------- | -------------------------------------- |
| Op          | .list::min                             |
| Args        | None                                   |
| Description | Returns the minimum value of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::min;
}
```

**Expected Output**

```json
"report": [
    3
  ]
```
### `idx_of_max`

|             |                                                     |
| ----------- | --------------------------------------------------- |
| Op          | .list::idx_of_max                                   |
| Args        | None                                                |
| Description | Returns the index of the maximum value of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::min;
}
```

**Expected Output**

```json
"report": [
    8
  ]
```

|             |                                                     |
| ----------- | --------------------------------------------------- |
| Op          | .list::idx_of_min                                   |
| Args        | None                                                |
| Description | Returns the index of the minimum value of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::idx_of_min;
}
```

**Expected Output**

```json
 "report": [
    3
  ]
```

### `copy`

|             |                                     |
| ----------- | ----------------------------------- |
| Op          | .list::copy                         |
| Args        | None                                |
| Description | Returns a shallow copy of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::copy;
}
```

**Expected Output**

```json
 "report": [
    [23,45,12,3,44,67,23,12,78]
  ],
```

### `deepcopy`

|             |                                  |
| ----------- | -------------------------------- |
| Op          | .list::deepcopy                  |
| Args        | None                             |
| Description | Returns a deep copy of the list. |


**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::deepcopy;
}
```

**Expected Output**

```json
 "report": [
    [23,45,12,3,44,67,23,12,78]
  ]
```

### `sort`

|             |                                                |
| ----------- | ---------------------------------------------- |
| Op          | .list::sort                                    |
| Args        | None                                           |
| Description | Sort the values in the list in ascending order |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::sort;
    report _list;
}
```

**Expected Output**

```json
"report": [
    [3,12,12,23,23,44,45,67,78]
  ]
```

### `reverse`

|             |                                |
| ----------- | ------------------------------ |
| Op          | .list::reverse                 |
| Args        | None                           |
| Description | Reverse the items in the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::reverse;
    report _list;
}
```

**Expected Output**

```json
"report": [
    [78,12,23,67,44,3,12,45,23]
  ]
```

### `clear`

|             |                                   |
| ----------- | --------------------------------- |
| Op          | .list::clear                      |
| Args        | None                              |
| Description | Clear all the values in the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::clear;
    report _list;
}
```

**Expected Output**

```json
 "report": [
    []
  ]
```

### `pop`

|             |                                   |
| ----------- | --------------------------------- |
| Op          | .list::pop                        |
| Args        | Optional                          |
| Description | Pops the last item from the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::pop;
    report _list;
}
```

**Expected Output**

```json
"report": [
    [23,45,12,3,44,67,23,12]
  ],
```

### `index`

|             |                                      |
| ----------- | ------------------------------------ |
| Op          | .list::index                         |
| Args        | Item from the list                   |
| Description | Returns the index of the given item. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::index(44);
}
```

**Expected Output**

```json
"report": [
    4
  ],
```

### `append`

|             |                                        |
| ----------- | -------------------------------------- |
| Op          | .list::append                          |
| Args        | A new item                             |
| Description | Append an new item in the end of list. |


**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::append(56);
    report _list;
}
```

**Expected Output**

```json
"report": [
    [23,45,12,3,44,67,23,12,78,56]
  ]
```

### `extend`

|             |                                                        |
| ----------- | ------------------------------------------------------ |
| Op          | .list::extend                                          |
| Args        | List of items                                          |
| Description | Concat list of values to the end of the existing list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::extend([56,34,72]);
    report _list;
}
```

**Expected Output**

```json
"report": [
    [23,45,12,3,44,67,23,12,78,56,34,72]
  ]
```

### `insert`

|             |                                                    |
| ----------- | -------------------------------------------------- |
| Op          | .list::insert                                      |
| Args        | index,value                                        |
| Description | Insert given value at the given index of the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::insert(2,34);
    report _list;
}
```


**Expected Output**
```json
"report": [
    [23,45,34,12,3,44,67,23,12,78]
  ]
```

### `remove`

|             |                                                                                                                   |
| ----------- | ----------------------------------------------------------------------------------------------------------------- |
| Op          | .list::remove                                                                                                     |
| Args        | Item from the list                                                                                                |
| Description | Remove the given value from the list. (If there are duplicates of the same value this removes only the first one) |


**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    _list.list::remove(12);
    report _list;
}
```
**Expected Output**

```json
  "report": [
    [23,45,3,44,67,23,12,78]
  ]
```

### `count`

|             |                                                       |
| ----------- | ----------------------------------------------------- |
| Op          | .list::count                                          |
| Args        | value                                                 |
| Description | Returns the number of occurrences of the given value. |


**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::count(12);
}
```

**Expected Output**

```json
 "report": [
    2
  ]
```

### `pairwise`

|             |                                                          |
| ----------- | -------------------------------------------------------- |
| Op          | .list::pairwise                                          |
| Args        | None                                                     |
| Description | Return successive overlapping pairs taken from the list. |

**Example Usage**

```jac
walker init{
    _list = [23,45,12,3,44,67,23,12,78];
    report _list.list::pairwise;
}
```

**Expected Output**

```json
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

### `unique`

|             |                                                 |
| ----------- | ----------------------------------------------- |
| Op          | .list::unique                                   |
| Args        | None                                            |
| Description | Return sorted list of unique items from a list. |

**Example Usage**

```jac
walker init{
    _list = [1,2,3,4,2,3,4,5];
    report _list.list::unique;
}
```

**Expected Output**

```json
"report": [
    [1,2,3,4,5]
  ],
```
