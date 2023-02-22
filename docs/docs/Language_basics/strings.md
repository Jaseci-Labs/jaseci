# Jaseci String Methods

In this section, the table below displays all of the **string** methods available in Jaseci for manipulating strings. These methods provide a comprehensive and efficient way to work with strings in your application.

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::upper | none | Convert the string into uppercase. |

**Example Usage**
```
walker init{
    _string = "Jaseci is an end-to-end open-source and Open Computational Model";
    report _string.str::upper;
}
```

**Expected Oputput**
```
"report": [
    "JASECI IS AN END-TO-END OPEN-SOURCE AND OPEN COMPUTATIONAL MODEL"
  ]
```


| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::lower | none | Convert the string into lowercase. |

**Example Usage**
```
walker init{
    _string = "Jaseci is an end-to-end open-source and Open Computational Model";
    report _string.str::lower;
}
```

**Expected Oputput**
```
"report": [
    "jaseci is an end-to-end open-source and open computational model"
  ]
```

| Op          | Args | Description                        |
| ----------- | ---- | ---------------------------------- |
| .str::title | none | Convert the string into camelcase. |

**Example Usage**
```
walker init{
    _string = "jaseci is an end-to-end open-source and open computational model";
    report _string.str::title;
}
```

**Expected Oputput**
```
"report": [
    "Jaseci Is An End-To-End Open-Source And Open Computational Model"
  ]
```

| Op               | Args | Description                                                    |
| ---------------- | ---- | -------------------------------------------------------------- |
| .str::capitalize | none | The first letter of the string will be converted into Capital. |

**Example Usage**
```
walker init{
    _string = "jaseci is an end-to-end open-source and open computational model";
    report _string.str::capitalize;
}
```

**Expected Oputput**
```
"report": [
    "Jaseci is an end-to-end open-source and open computational model"
  ],
```

| Op              | Args | Description |
| --------------- | ---- | ----------- |
| .str::swap_case | none |             |

**Example Usage**
```
walker init{
    _string = "Jaseci is an End-to-End Open-Source and Open Computational Model";
    report _string.str::swap_case;
}
```

**Expected Oputput**
```
  "report": [
    "jASECI IS AN eND-TO-eND oPEN-sOURCE AND oPEN cOMPUTATIONAL mODEL"
  ],
```

| Op             | Args | Description                                   |
| -------------- | ---- | --------------------------------------------- |
| .str::is_alnum | none | Return true if the string is alpha numerical. |

**Example Usage**
```
walker init{
    _string = "123";
    report _string.str::is_alnum;
}
```

**Expected Oputput**
```
 "report": [
    true
  ],
```

| Op             | Args | Description                             |
| -------------- | ---- | --------------------------------------- |
| .str::is_digit | none | Returns true if string contains digits. |

**Example Usage**
```
walker init{
    _string = "123";
    report _string.str::is_digit;
}
```

**Expected Oputput**
```
 "report": [
    true
  ]
```

| Op             | Args | Description                                               |
| -------------- | ---- | --------------------------------------------------------- |
| .str::is_title | none | Return true if the first letter of the string is capital. |

**Example Usage**
```
walker init{
    _string = "Hello world";
    report _string.str::is_title;
}
```

**Expected Oputput**
```
"report": [
    true
  ]
```

| Op             | Args | Description                                             |
| -------------- | ---- | ------------------------------------------------------- |
| .str::is_upper | none | Return true if all characters in the string is in Caps. |

**Example Usage**
```
walker init{
    _string = "HELLO WORLD";
    report _string.str::is_upper;
}
```

**Expected Oputput**
```
"report": [
    true
  ],
```

| Op             | Args | Description                                                   |
| -------------- | ---- | ------------------------------------------------------------- |
| .str::is_lower | none | Return true if all characters in the string is in lower case. |

**Example Usage**

```
walker init{
    _string = "hello world";
    report _string.str::is_lower;
}
```

**Expected Oputput**
```
"report": [
    true
  ],
```

| Op             | Args | Description                                           |
| -------------- | ---- | ----------------------------------------------------- |
| .str::is_space | none | Return true if the string contains only white spaces. |

**Example Usage**
```
walker init{
    _string = "   ";
    report _string.str::is_space;
}
```

**Expected Oputput**
```
"report": [
    true
  ]
```

| Op              | Args | Description |
| --------------- | ---- | ----------- |
| .str::load_json | none |             |

**Example Usage**
```
```

**Expected Oputput**
```
```

| Op          | Args               | Description                                                                                                             |
| ----------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| .str::count | substr, start, end | Returns the number of occurrences of a sub-string in the given string. Start and end specify range of indices to search |

**Example Usage**
```
walker init{
    _string = "Hello World";
    report _string.str::count("l",0,11);
}
```

**Expected Oputput**
```
 "report": [
    3
  ]
```



| Op         | Args               | Description                                                                                                                                       |
| ---------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| .str::find | substr, start, end | Returns the index of first occurrence of the substring (if found). If not found, it returns -1. Start and end specify range of indices to search. |

**Example Usage**

```
walker init{
    _string = "Hello World";
    report _string.str::find("l");
}
```

**Expected Oputput**

```
"report": [
    2
]
```

| Op          | Args                          | Description                                                                                                                                                   |
| ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| .str::split | optional (separator,maxsplit) | Breaks up a string at the specified separator formaxsplit number of times and returns a list of strings. Default separators is ‘ ’ and maxsplit is unlimited. |

**Example Usage**
```
walker init{
    _string = "Hello World";
    report _string.str::split("l");
}
```

**Expected Oputput**
```
"report": [
    [
      "He",
      "",
      "o Wor",
      "d"
    ]
  ]
```


| Op         | Args   | Description                                                                                            |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------ |
| .str::join | params | Join elements of the sequence (params) separated by the string separator that calls the join function. |

**Example Usage**
```

```

**Expected Oputput**
```
```

| Op               | Args | Description |
| ---------------- | ---- | ----------- |
| .str::startswith |      |             |


**Example Usage**
```
```

**Expected Oputput**
```
```

| Op             | Args | Description |
| -------------- | ---- | ----------- |
| .str::endswith |      |             |

**Example Usage**
```
```

**Expected Oputput**
```
```

| Op            | Args | Description |
| ------------- | ---- | ----------- |
| .str::replace |      |             |

**Example Usage**
```
```

**Expected Oputput**
```
```

| Op          | Args     | Description |
| ----------- | -------- | ----------- |
| .str::strip | optional |             |

**Example Usage**
```
```

**Expected Oputput**
```
```

| Op           | Args     | Description |
| ------------ | -------- | ----------- |
| .str::lstrip | optional |             |

**Example Usage**
```
```

**Expected Oputput**
```
```

| Op           | Args     | Description |
| ------------ | -------- | ----------- |
| .str::rstrip | optional |             |

**Example Usage**
```
```

**Expected Oputput**
```
```
