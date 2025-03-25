## Introduction

### Basic Structure
Sets are a type of data structure used to store multiple items in one variable. Along with List, Tuple, and Dictionary, sets are one of Python's four built-in data types for handling collections. A set is unique in that it is unordered, unchangeable, and does not use indexing.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:2:5"
    ```

### Set Items
Set items are unordered, unchangeable, and do not allow duplicate values.

### Unordered
Unordered means that the items in a set do not follow a specific order. Each time you use a set, its items may appear in a different order, and they cannot be accessed using an index or key.

### Unchangeable
Set items are unchangeable, meaning that we cannot change the items after the set has been created.

### Duplicates Not Allowed
Sets cannot have two items with the same value.

## Access Set Items

### Access Items
Items in a set cannot be accessed via an index or key. However, you can iterate over the items with a **for** loop or check if a specific value exists in the set using the **in** keyword.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:8:13"
    ```

### Check Items
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:15:18"
    ```

## Add Set Items

### Add Items
**1.Using Add( ) method**

To add one item to a set use the **add()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:21:25"
    ```

**2.Using update( ) method**

To add items from another set into the current set, use the **update()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:27:34"
    ```

### Add Any Iterable

The object in the **update()** method does not have to be a set, it can be any iterable object (tuples, lists, dictionaries etc.).

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:36:43"
    ```

## Remove Set Items

### Remove Item
To remove an item in a set, use the **remove()**, or the **discard()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:47:51"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:53:57"
    ```

You can also use the **pop()** method to remove an item, but this method will remove a random item, so you cannot be sure what item that gets removed.The return value of the **pop()** method is the removed item.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:59:64"
    ```

The **clear()** method removes all items from a set, leaving it empty.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:66:70"
    ```
The **del** keyword deletes a set entirely. After using **del**, the set no longer exists.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:72:75"
    ```

## Loop Sets

### Loop Items

You can loop through the set items by using a for loop:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:79:84"
    ```

## Join Sets

There are several ways to join two or more sets in Python.

- The **union( )** and **update( )** methods joins all items from both sets.
- The **intersection( )** method keeps ONLY the duplicates.
- The **difference( )** method keeps the items from the first set that are not in the other set(s).

### Union

The **union()** method returns a new set with all items from both sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:87:93"
    ```

You can use the **|** operator instead of the **union()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:95:101"
    ```

### Join Multiple Sets

All the joining methods and operators can be used to join multiple sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:103:111"
    ```

When using the | operator, separate the sets with more | operators:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:113:121"
    ```

### Update

The update() method inserts all items from one set into another.The update() changes the original set, and does not return a new set.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:123:129"
    ```

### Intersection

The intersection() method will return a new set, that only contains the items that are present in both sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:131:137"
    ```
You can use the **&** operator instead of the **intersection()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:139:145"
    ```

### Difference

The **difference()** method will return a new set that will contain only the items from the first set that are not present in the other set.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:147:154"
    ```

You can use the **-** operator instead of the **difference()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets.jac:156:163"
    ```