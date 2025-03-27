Tuples store multiple items in one variable.They are ordered, unchangeable, and use round brackets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:2:5"
    ```

### Tuple Items
Tuple items are ordered, unchangeable, and allow duplicate values.Tuple items are indexed, the first item has index [0], the second item has index [1] etc.

### Ordered
When we say that tuples are ordered, it means that the items have a defined order, and that order will not change.

### Unchangeable
Tuples are unchangeable, meaning that we cannot change, add or remove items after the tuple has been created.

### Allow Duplicates
Since tuples are indexed, they can have items with the same value:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:7:10"
    ```

### Tuple Length
To determine how many items a tuple has, use the **len()** function:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:12:15"
    ```

## Access Tuple Items
You can access tuple items by referring to the index number, inside square brackets:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:18:21"
    ```

### Negative Indexing
Negative indexing means start from the end.**-1** refers to the last item, **-2** refers to the second last item etc.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:23:26"
    ```

### Range of Indexes
You can specify a range of indexes by specifying where to start and where to end the range.When specifying a range, the return value will be a new tuple with the specified items.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:28:31"
    ```
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:33:36"
    ```

### Check if Item Exists
To determine if a specified item is present in a tuple use the **in** keyword:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:38:43"
    ```

## Update Tuple Items

### Change Tuple Values
Once a tuple is created, you cannot change its values. Tuples are **unchangeable**, or **immutable** as it also is called.But there is a workaround. You can convert the tuple into a list, change the list, and convert the list back into a tuple.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:46:53"
    ```

### Add Items
Since tuples are immutable, they do not have a built-in **append()** method, but there are other ways to add items to a tuple.

**1. Convert into a list:**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:55:60"
    ```

**2. Add tuple to a tuple:**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:62:67"
    ```

### Remove Items
Tuples are **unchangeable**, so you cannot remove items from it, but you can use the same workaround as we used for changing and adding tuple items:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:69:74"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:76:79"
    ```

## Unpack Tuple Items
Tuples can be 'packed' by assigning values to them. In Python, we can also 'unpack' a tuple by extracting its values into individual variables.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:82:89"
    ```

### Using Asterisk *
If the number of variables is less than the number of values, you can add an * to the variable name and the values will be assigned to the variable as a list:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:91:98"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:100:108"
    ```

## Loop Tuple

### Loop Through a Tuple
You can loop through the tuple items by using a **for** loop.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:111:116"
    ```

### Loop Through the Index Numbers
You can also loop through the tuple items by referring to their index number.Use the **range()** and **len()** functions to create a suitable iterable.

**1.Using a for Loop**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:118:123"
    ```

**1.Using a while Loop**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:125:132"
    ```

## Join Tuples

### Join Two Tuples
To join two or more tuples you can use the **+** operator:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:135:141"
    ```

### Multiply Tuples
If you want to multiply the content of a tuple a given number of times, you can use the * operator:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple.jac:143:148"
    ```
