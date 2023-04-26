---
sidebar_position: 3
title: Strings
description: Methods available in Jaseci for manipulating strings.
---

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
