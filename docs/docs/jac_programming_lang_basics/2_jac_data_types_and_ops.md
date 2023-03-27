# Data Types in Jaseci

In this section, we delve into the powerful tools that Jaseci provides for manipulating various data structures. Specifically, we will be exploring the methods available for manipulating strings, dictionaries, and lists. These methods are essential for any programmer looking to efficiently and effectively manage data in their applications. Whether you are a beginner or an experienced developer, understanding these methods will be key to your success in using Jaseci. So sit back, get ready to learn, and let's dive into the exciting world of Jaseci data manipulation!

- [Data Types in Jaseci](#data-types-in-jaseci)
  - [Dictionaries](#dictionaries)
    - [`items`](#items)
    - [`copy`](#copy)
    - [`deepcopy`](#deepcopy)
    - [`keys`](#keys)
    - [`clear`](#clear)
    - [`popitem`](#popitem)
    - [`values`](#values)
    - [`pop`](#pop)
    - [`update`](#update)
  - [List](#list)
    - [`max`](#max)
    - [`min`](#min)
    - [`idx_of_max`](#idx_of_max)
    - [`idx_of_min`](#idx_of_min)
    - [`copy`](#copy-1)
    - [`deepcopy`](#deepcopy-1)
    - [`sort`](#sort)
    - [`reverse`](#reverse)
    - [`clear`](#clear-1)
    - [`pop`](#pop-1)
    - [`index`](#index)
    - [`append`](#append)
    - [`extend`](#extend)
    - [`insert`](#insert)
    - [`remove`](#remove)
    - [`count`](#count)
    - [`pairwise`](#pairwise)
    - [`unique`](#unique)
  - [Strings](#strings)
    - [`upper`](#upper)
    - [`lower`](#lower)
    - [`title`](#title)
    - [`capitalize`](#capitalize)
    - [`swap_case`](#swap_case)
    - [`is_alnum`](#is_alnum)
    - [`is_digit`](#is_digit)
    - [`is_title`](#is_title)
    - [`is_upper`](#is_upper)
    - [`is_lower`](#is_lower)
    - [`is_space`](#is_space)
    - [`load_json`](#load_json)
    - [`count`](#count-1)
    - [`find`](#find)
    - [`split`](#split)
    - [`join`](#join)
    - [`statswith`](#statswith)
    - [`endswith`](#endswith)
    - [`replace`](#replace)
    - [`strip`](#strip)
    - [`lstrip`](#lstrip)
    - [`rstrip`](#rstrip)

## Dictionaries


In this section below, displays all of the **Dictionary** methods available in Jaseci for manipulating dictionaries. These methods provide a comprehensive and efficient way to work with dictionaries in your application.

### `items`

| Op           | Args         | Description                                       |
| ------------ | ------------ | ------------------------------------------------- |
| .dict::items | key, default | Returns value of key if exists otherwise default. |

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

### `copy`

| Op          | Args | Description                               |
| ----------- | ---- | ----------------------------------------- |
| .dict::copy | none | Returns a shallow copy of the dictionary. |

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

| Op              | Args | Description                            |
| --------------- | ---- | -------------------------------------- |
| .dict::deepcopy | none | Returns a deep copy of the dictionary. |

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

### `keys`

| Op          | Args | Description                    |
| ----------- | ---- | ------------------------------ |
| .dict::keys | none | Return keys of the dictionary. |

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

### `clear`

| Op           | Args | Description                                      |
| ------------ | ---- | ------------------------------------------------ |
| .dict::clear | none | Clears all the keys and values in the dictonary. |

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

### `popitem`

| Op             | Args | Description                                       |
| -------------- | ---- | ------------------------------------------------- |
| .dict::popitem | none | Pops the last key value pair from the dictionary. |

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
### `values`

| Op            | Args | Description                              |
| ------------- | ---- | ---------------------------------------- |
| .dict::values | none | Return all the values in the dictionary. |

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

### `pop`

| Op         | Args                | Description                                               |
| ---------- | ------------------- | --------------------------------------------------------- |
| .dict::pop | A key from the dict | Pops the value from the dictionary where the key is given |

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
| Op            | Args                       | Description                     |
| ------------- | -------------------------- | ------------------------------- |
| .dict::update | Dict {"key" : "new value"} | Updates items in the dictionary |

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

## List


In this section you will find all of the **list** methods available in Jaseci for manipulating lists. These methods provide a comprehensive and efficient way to work with lists in your application.

### `max`

| Op         | Args | Description                            |
| ---------- | ---- | -------------------------------------- |
| .list::max | none | Returns the maximum value of the list. |

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

| Op         | Args | Description                            |
| ---------- | ---- | -------------------------------------- |
| .list::min | none | Returns the minimum value of the list. |

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

| Op                | Args | Description                                         |
| ----------------- | ---- | --------------------------------------------------- |
| .list::idx_of_max | none | Returns the index of the maximum value of the list. |

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

### `idx_of_min`
| Op                | Args | Description                                         |
| ----------------- | ---- | --------------------------------------------------- |
| .list::idx_of_min | none | Returns the index of the minimum value of the list. |

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

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .list::copy | none | Returns a shallow copy of the list |

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

| Op              | Args | Description                     |
| --------------- | ---- | ------------------------------- |
| .list::deepcopy | none | Returns a deep copy of the list |

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

| Op          | Args | Description                                    |
| ----------- | ---- | ---------------------------------------------- |
| .list::sort | none | Sort the values in the list in assending order |

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
| Op             | Args | Description                    |
| -------------- | ---- | ------------------------------ |
| .list::reverse | none | Reverse the items in the list. |

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

| Op           | Args | Description                      |
| ------------ | ---- | -------------------------------- |
| .list::clear | none | Clear all the values in the list |

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

| Op         | Args     | Description                       |
| ---------- | -------- | --------------------------------- |
| .list::pop | optional | Pops the last item from the list. |

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

| Op           | Args            | Description                           |
| ------------ | --------------- | ------------------------------------- |
| .list::index | value from list | Returns the index of the given value. |

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

| Op            | Args        | Description                             |
| ------------- | ----------- | --------------------------------------- |
| .list::append | a new value | Append an new value in the end of list. |

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

| Op            | Args           | Description                                            |
| ------------- | -------------- | ------------------------------------------------------ |
| .list::extend | list of values | Concat list of values to the end of the existing list. |


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

| Op            | Args        | Description                                        |
| ------------- | ----------- | -------------------------------------------------- |
| .list::insert | index,value | Insert given value at the given index of the list. |

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
| Op            | Args  | Description                                                                                                       |
| ------------- | ----- | ----------------------------------------------------------------------------------------------------------------- |
| .list::remove | value | Remove the given value from the list. (If there are duplicates of the same value this removes only the first one) |

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
| Op           | Args  | Description                                          |
| ------------ | ----- | ---------------------------------------------------- |
| .list::count | value | Returns the number of occurences of the given value. |


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

| Op              | Args | Description                                              |
| --------------- | ---- | -------------------------------------------------------- |
| .list::pairwise | none | Return successive overlapping pairs taken from the list. |

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

| Op            | Args | Description                                     |
| ------------- | ---- | ----------------------------------------------- |
| .list::unique | none | Return sorted list of unique items from a list. |


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

## Strings

In this section displays all of the **string** methods available in Jaseci for manipulating strings. These methods provide a comprehensive and efficient way to work with strings in your application.

### `upper`

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::upper | none | Convert the string into uppercase. |

**Example Usage**

```jac
walker init{
    _string = "Jaseci is an end-to-end open-source and Open Computational Model";
    report _string.str::upper;
}
```

**Expected Oputput**

```json
"report": [
    "JASECI IS AN END-TO-END OPEN-SOURCE AND OPEN COMPUTATIONAL MODEL"
  ]
```


### `lower`

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::lower | none | Convert the string into lowercase. |

**Example Usage**

```jac
walker init{
    _string = "Jaseci is an end-to-end open-source and Open Computational Model";
    report _string.str::lower;
}
```

**Expected Oputput**

```json
"report": [
    "jaseci is an end-to-end open-source and open computational model"
  ]
```

### `title`

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::title | none | Convert the string into camelcase. |

**Example Usage**

```jac
walker init{
    _string = "jaseci is an end-to-end open-source and open computational model";
    report _string.str::title;
}
```

**Expected Oputput**

```json
"report": [
    "Jaseci Is An End-To-End Open-Source And Open Computational Model"
  ]
```

### `capitalize`

| Op               | Args | Description                                                    |
| ---------------- | ---- | -------------------------------------------------------------- |
| .str::capitalize | none | The first letter of the string will be converted into Capital. |

**Example Usage**

```jac
walker init{
    _string = "jaseci is an end-to-end open-source and open computational model";
    report _string.str::capitalize;
}
```

**Expected Oputput**

```json
"report": [
    "Jaseci is an end-to-end open-source and open computational model"
  ],
```

### `swap_case`
| Op              | Args | Description |
| --------------- | ---- | ----------- |
| .str::swap_case | none |             |

**Example Usage**

```jac
walker init{
    _string = "Jaseci is an End-to-End Open-Source and Open Computational Model";
    report _string.str::swap_case;
}
```

**Expected Oputput**

```json
  "report": [
    "jASECI IS AN eND-TO-eND oPEN-sOURCE AND oPEN cOMPUTATIONAL mODEL"
  ],
```

### `is_alnum`

| Op             | Args | Description                                   |
| -------------- | ---- | --------------------------------------------- |
| .str::is_alnum | none | Return true if the string is alpha numerical. |

**Example Usage**

```jac
walker init{
    _string = "123";
    report _string.str::is_alnum;
}
```

**Expected Oputput**

```json
 "report": [
    true
  ],
```

### `is_digit`

| Op             | Args | Description                             |
| -------------- | ---- | --------------------------------------- |
| .str::is_digit | none | Returns true if string contains digits. |

**Example Usage**

```jac
walker init{
    _string = "123";
    report _string.str::is_digit;
}
```

**Expected Oputput**

```json
 "report": [
    true
  ]
```

### `is_title`

| Op             | Args | Description                                               |
| -------------- | ---- | --------------------------------------------------------- |
| .str::is_title | none | Return true if the first letter of the string is capital. |

**Example Usage**

```jac
walker init{
    _string = "Hello world";
    report _string.str::is_title;
}
```

**Expected Oputput**

```json
"report": [
    true
  ]
```

### `is_upper`

| Op             | Args | Description                                             |
| -------------- | ---- | ------------------------------------------------------- |
| .str::is_upper | none | Return true if all characters in the string is in Caps. |

**Example Usage**

```jac
walker init{
    _string = "HELLO WORLD";
    report _string.str::is_upper;
}
```

**Expected Oputput**

```json
"report": [
    true
  ],
```

### `is_lower`

| Op             | Args | Description                                                   |
| -------------- | ---- | ------------------------------------------------------------- |
| .str::is_lower | none | Return true if all characters in the string is in lower case. |

**Example Usage**

```jac
walker init{
    _string = "hello world";
    report _string.str::is_lower;
}
```

**Expected Oputput**

```json
"report": [
    true
  ],
```

### `is_space`

| Op             | Args | Description                                           |
| -------------- | ---- | ----------------------------------------------------- |
| .str::is_space | none | Return true if the string contains only white spaces. |

**Example Usage**

```jac
walker init{
    _string = "   ";
    report _string.str::is_space;
}
```

**Expected Oputput**

```json
"report": [
    true
  ]
```

### `load_json`

| Op              | Args | Description |
| --------------- | ---- | ----------- |
| .str::load_json | none |             |

**Example Usage**

```jac

```

**Expected Oputput**

```json

```


### `count`

| Op          | Args               | Description                                                                                                             |
| ----------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| .str::count | substr, start, end | Returns the number of occurrences of a sub-string in the given string. Start and end specify range of indices to search |

**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::count("l",0,11);
}
```

**Expected Oputput**

```json
 "report": [
    3
  ]
```

### `find`

| Op         | Args               | Description                                                                                                                                       |
| ---------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| .str::find | substr, start, end | Returns the index of first occurrence of the substring (if found). If not found, it returns -1. Start and end specify range of indices to search. |

**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::find("l");
}
```

**Expected Oputput**

```json
"report": [
    2
]
```


### `split`

| Op          | Args                          | Description                                                                                                                                                   |
| ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| .str::split | optional (separator,maxsplit) | Breaks up a string at the specified separator formaxsplit number of times and returns a list of strings. Default separators is ‘ ’ and maxsplit is unlimited. |

**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::split("l");
}
```

**Expected Oputput**

```json
"report": [
    [
      "He",
      "",
      "o Wor",
      "d"
    ]
  ]
```

### `join`
| Op         | Args   | Description                                                                                            |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------ |
| .str::join | params | Join elements of the sequence (params) separated by the string separator that calls the join function. |

**Example Usage**

```jac
walker init{
    _list = ["Hello", "World"];
    report " ".str::join(_list);
}
```

**Expected Oputput**

```json
"report": [
    "Hello World"
  ]
```

### `statswith`

| Op               | Args   | Description                                                |
| ---------------- | ------ | ---------------------------------------------------------- |
| .str::startswith | params | Return true if the string starts with the given substring. |


**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::startswith("H");
}
```

**Expected Oputput**

```json
"report": [
    true
  ]
```


### `endswith`

| Op             | Args   | Description                                              |
| -------------- | ------ | -------------------------------------------------------- |
| .str::endswith | params | Return true if the string ends with the given substring. |

**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::endsswith("d");
}
```

**Expected Oputput**

```json
"report": [
    true
  ]
```

### `replace`

| Op            | Args   | Description                                  |
| ------------- | ------ | -------------------------------------------- |
| .str::replace | params | Replace the string with the given substring. |

**Example Usage**

```jac
walker init{
    _string = "Hello World";
    report _string.str::replace("World", "Jaseci");
}
```

**Expected Oputput**

```json
"report": [
    "Hello Jaseci"
  ]
```

### `strip`

| Op          | Args     | Description                                                                                                                                   |
| ----------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| .str::strip | optional | Removes any leading (spaces at the beginning) and trailing (spaces at the end) characters (space is the default leading character to remove). |

**Example Usage**

```jac
walker init{
    _string = "  Hello World  ";
    report _string.str::strip;
}
```

**Expected Oputput**

```json
"report": [
    "Hello World"
  ]
```

### `lstrip`

| Op           | Args     | Description                                                                                                  |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------------ |
| .str::lstrip | optional | Removes any leading (spaces at the beginning) characters (space is the default leading character to remove). |

**Example Usage**

```jac
walker init{
    _string = "  Hello World  ";
    report _string.str::lstrip;
}
```

**Expected Oputput**

```json
"report": [
    "Hello World  "
  ]
```

### `rstrip`

| Op           | Args     | Description                                                                                         |
| ------------ | -------- | --------------------------------------------------------------------------------------------------- |
| .str::rstrip | optional | Removes trailing (spaces at the end) characters (space is the default leading character to remove). |

**Example Usage**

```jac
walker init{
    _string = "  Hello World  ";
    report _string.str::rstrip;
}
```

**Expected Oputput**
```json
"report": [
    "  Hello World"
  ]
```
