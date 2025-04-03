## Introduction

### Basic Dictionary
Dictionaries are used to store data values in `key:value` pairs.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:2:5"
    ```

### Dictionary Items
Dictionary items are ordered, changeable, and do not allow duplicates.Dictionary items are presented in `key:value` pairs, and can be referred to by using the key name.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:7:10"
    ```

### Ordered
In JacLang, dictionaries are ordered, meaning key-value pairs retain their insertion order. This ensures predictable access and iteration over elements. Unlike lists, dictionary items cannot be accessed by index but must be referenced using their unique keys.

### Changeable

Dictionaries are changeable, meaning that we can change, add or remove items after the dictionary has been created.

### Duplicates Not Allowed

Dictionaries cannot have two items with the same key:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:12:15"
    ```

### Dictionary Length

To determine how many items a dictionary has, use the `len()` function:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:17:20"
    ```

## Access Items
You can access the items of a dictionary by referring to its key name, inside square brackets:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:24:27"
    ```

There is also a method called get() that will give you the same result:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:29:32"
    ```

### Get Keys

The `keys()` method will return a list of all the keys in the dictionary.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:34:38"
    ```

### Get Values

The `values()` method will return a list of all the values in the dictionary.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:40:44"
    ```

### Get Items
The `items()` method will return each item in a dictionary, as tuples in a list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:46:50"
    ```

### Check if Key Exists

To determine if a specified key is present in a dictionary use the in keyword:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:52:59"
    ```

## Change Items

### Change Values
You can change the value of a specific item by referring to its key name:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:63:67"
    ```

### Update Dictionary

The **update()** method will update the dictionary with the items from the given argument.The argument must be a dictionary, or an iterable object with `key:value` pairs.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:69:73"
    ```

## Add Items

### Add Items
Adding an item to the dictionary is done by using a new index key and assigning a value to it:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:77:81"
    ```

### Update Dictionary

The **update()** method will update the dictionary with the items from a given argument. If the item does not exist, the item will be added.The argument must be a dictionary, or an iterable object with key:value pairs.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:83:87"
    ```

## Remove Items

There are several methods to remove items from a dictionary:

The **pop()** method removes the item with the specified key name:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:91:95"
    ```

The **popitem()** method removes the last inserted item:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:97:101"
    ```

The **del** keyword removes the item with the specified key name:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:103:107"
    ```

The **clear()** method empties the dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:109:113"
    ```

## Loop Dictionaries

You can loop through a dictionary by using a for loop.When looping through a dictionary, the return value are the keys of the dictionary, but there are methods to return the values as well.

Print all key names in the dictionary, one by one:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:117:122"
    ```

Print all values in the dictionary, one by one:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:124:129"
    ```

You can also use the **values()** method to return values of a dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:131:136"
    ```

You can use the **keys()** method to return the keys of a dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:138:143"
    ```

Loop through both keys and values, by using the **items()** method:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:145:150"
    ```

## Copy Dictionaries

You cannot copy a dictionary simply by typing `dict2 = dict1`, because: `dict2` will only be a reference to `dict1`, and changes made in `dict1` will automatically also be made in `dict2`.

There are ways to make a copy, one way is to use the built-in Dictionary method **copy()**.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:154:158"
    ```

Another way to make a copy is to use the built-in function `dict()`.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:160:164"
    ```

## Nested Dictionaries

A dictionary can contain dictionaries, this is called nested dictionaries.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:168:175"
    ```

Create three dictionaries, then create one dictionary that will contain the other three dictionaries:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:177:184"
    ```

### Access Items in Nested Dictionaries

To access items from a nested dictionary, you use the name of the dictionaries, starting with the outer dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary.jac:186:193"
    ```