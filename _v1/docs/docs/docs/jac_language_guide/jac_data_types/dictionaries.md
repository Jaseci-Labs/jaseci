---
sidebar_position: 1
title: Dictionaries
description: Methods available in Jaseci for manipulating dictionaries.
---

# Dictionaries

In this section below, displays all of the **Dictionary** methods available in Jaseci for manipulating dictionaries. These methods provide a comprehensive and efficient way to work with dictionaries in Jac program.

### `items`


|             |                                                   |
| ----------- | ------------------------------------------------- |
| Op          | .dict::items                                      |
| Args        | key, default                                      |
| Description | Returns value of key if exists otherwise default. |


**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::items;
}
```

**Expected Output**
```json
"report": [
    [
      ["key1","value1"],
      ["key2","value2"],
      ["key3","value3"]
    ]
  ]
```
### `keys`

|             |                                |
| ----------- | ------------------------------ |
| Op          | .dict::keys                    |
| Args        | None                           |
| Description | Return keys of the dictionary. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::keys;
}
```

**Expected Output**

```jac
 "report": [
    ["key1","key2","key3"]
  ]
```

### `values`

|             |                                          |
| ----------- | ---------------------------------------- |
| Op          | .dict::values                            |
| Args        | None                                     |
| Description | Return all the values in the dictionary. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::values;
}
```

**Expected Output**

```json
"report": [
    [
      "value1",
      "value2",
      "value3"
    ]
  ]
```

### `copy`

|             |                                           |
| ----------- | ----------------------------------------- |
| Op          | .dict::copy                               |
| Args        | None                                      |
| Description | Returns a shallow copy of the dictionary. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict_copy = _dict.dict::copy;

    report _dict_copy;
}
```
**Expected Output**

```json
 "report" : [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value3"
    }
  ]
```

### `deepcopy`

|             |                                        |
| ----------- | -------------------------------------- |
| Op          | .dict::deepcopy                        |
| Args        | None                                   |
| Description | Returns a deep copy of the dictionary. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict_deepcopy = _dict.dict::deepcopy ;

    report _dict_deepcopy;
}
```

**Expected Output**

```json
"report": [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value3"
    }
  ]
```

### `popitem`

|             |                                                   |
| ----------- | ------------------------------------------------- |
| Op          | .dict::popitem                                    |
| Args        | None                                              |
| Description | Pops the last key value pair from the dictionary. |


**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::popitem;
    report _dict;
}
```

**Expected Output**

```json
"report": [
    {
      "key1": "value1",
      "key2": "value2"
    }
  ]
```

### `pop`

|             |                                                            |
| ----------- | ---------------------------------------------------------- |
| Op          | .dict::pop                                                 |
| Args        | A key from the dict                                        |
| Description | Pops the value from the dictionary where the key is given. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::pop("key1");
    report _dict;
}
```

**Expected Output**

```json
"report": [
    {
      "key2": "value2",
      "key3": "value3"
    }
]
```

### `update`

|             |                                                      |
| ----------- | ---------------------------------------------------- |
| Op          | .dict::update                                        |
| Args        | Dictionary object. (Ex: Dict {"key" : "new value"})  |
| Description | Updates items in the dictionary item with new value. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::update({'key3': "value4"});
    report _dict;
}
```

**Expected Output**

```json
  "report": [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value4"
    }
  ]
```


### `clear`

|             |                                                   |
| ----------- | ------------------------------------------------- |
| Op          | .dict::clear                                      |
| Args        | None                                              |
| Description | Clears all the keys and values in the dictionary. |

**Example Usage**

```jac
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::clear;
}
```

**Expected Output**

```json
"report": [
    null
  ]
```