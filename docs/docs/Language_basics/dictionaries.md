# Jaseci Dictionary Methods

In this section, the table below displays all of the **Dictionary** methods available in Jaseci for manipulating dictionaries. These methods provide a comprehensive and efficient way to work with dictionaries in your application.

| Op           | Args         | Description                                       |
| ------------ | ------------ | ------------------------------------------------- |
| .dict::items | key, default | Returns value of key if exists otherwise default. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::items;
}
```

**Expected Output**
```
"report": [
    [
      ["key1","value1"],
      ["key2","value2"],
      ["key3","value3"]
    ]
  ]
```

| Op          | Args | Description                               |
| ----------- | ---- | ----------------------------------------- |
| .dict::copy | none | Returns a shallow copy of the dictionary. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict_copy = _dict.dict::copy;

    report _dict_copy;
}
```
**Expected Output**
```
 "report" : [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value3"
    }
  ]
```


| Op              | Args | Description                            |
| --------------- | ---- | -------------------------------------- |
| .dict::deepcopy | none | Returns a deep copy of the dictionary. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict_deepcopy = _dict.dict::deepcopy ;

    report _dict_deepcopy;
}
```
**Expected Output**
```
"report": [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value3"
    }
  ]
```

| Op          | Args | Description                    |
| ----------- | ---- | ------------------------------ |
| .dict::keys | none | Return keys of the dictionary. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::keys;
}
```

**Expected Output**
```
 "report": [
    ["key1","key2","key3"]
  ]
```

| Op           | Args | Description                                      |
| ------------ | ---- | ------------------------------------------------ |
| .dict::clear | none | Clears all the keys and values in the dictonary. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::clear;
}
```

**Expected Output**
```
"report": [
    null
  ]
```

| Op             | Args | Description                                       |
| -------------- | ---- | ------------------------------------------------- |
| .dict::popitem | none | Pops the last key value pair from the dictionary. |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::popitem;
    report _dict;
}
```

**Expected Output**
```
"report": [
    {
      "key1": "value1",
      "key2": "value2"
    }
  ]
```


| Op            | Args | Description                              |
| ------------- | ---- | ---------------------------------------- |
| .dict::values | none | Return all the values in the dictionary. |

**Example Usage**
```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    report _dict.dict::values;
}
```
**Expected Output**
```
"report": [
    [
      "value1",
      "value2",
      "value3"
    ]
  ]
```

| Op         | Args                | Description                                               |
| ---------- | ------------------- | --------------------------------------------------------- |
| .dict::pop | A key from the dict | Pops the value from the dictionary where the key is given |

**Example Usage**
```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::pop("key1");
    report _dict;
}
```

**Expected Output**
```
"report": [
    {
      "key2": "value2",
      "key3": "value3"
    }
```

| Op            | Args                       | Description                     |
| ------------- | -------------------------- | ------------------------------- |
| .dict::update | Dict {"key" : "new value"} | Updates items in the dictionary |

**Example Usage**

```
walker init{
    _dict = {"key1":"value1", "key2":"value2", "key3":"value3"};
    _dict.dict::update({'key3': "value4"});
    report _dict;
}
```

**Expected Output**
```
  "report": [
    {
      "key1": "value1",
      "key2": "value2",
      "key3": "value4"
    }
```