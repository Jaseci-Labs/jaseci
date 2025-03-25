## Introduction
### Basic List
Since lists are indexed, lists can have items with the same value:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:2:5"
    ```

### List Items
List items are ordered, changeable, and allow duplicate values.
List items are indexed, the first item has index **[0]**, the second item has index **[1]** etc.

### Ordered
Lists maintain a specific sequence, meaning each item has a fixed position that remains unchanged.
When new elements are added to a list, they are automatically appended to the end, preserving the original order of existing items.

### Changeable
The list is changeable, meaning that we can change, add, and remove items in a list after it has been created.

### Allow Duplicates
Since lists are indexed, lists can have items with the same value:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:7:10"
    ```

### List Length
To determine how many items a list has, use the len() function:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:12:15"
    ```

### List Items - Data Types
List items can be of any data type:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:17:21"
    ```

A list can contain different data types:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:23:26"
    ```

### The List Constructor
It is also possible to use the **list()** constructor when creating a new list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:28:31"
    ```

## Access List Items
### Access Items
List items are indexed and you can access them by referring to the index number:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:34:37"
    ```

### Negative Indexing
Negative indexing means start from the end **-1** refers to the last item, **-2** refers to the second last item etc.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:39:42"
    ```

### Range of Indexes
In Jac, you can work with lists using index ranges to extract specific portions of data.You can specify a range of indexes by defining where to start and where to end.The result will be a new list containing the specified elements.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:44:47"
    ```

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:49:52"
    ```
**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:54:57"
    ```

### Check if Item Exists
To determine if a specified item is present in a list use the **in** keyword:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:59:64"
    ```

## Change List Items
### Change Item Value
To change the value of a specific item, refer to the index number:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:67:71"
    ```

### Change a Range of Item Values
To change the value of items within a specific range, define a list with the new values, and refer to the range of index numbers where you want to insert the new values:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:73:77"
    ```

### Insert Items
To insert a new list item, without replacing any of the existing values, we can use the **insert()** method.The **insert()** method inserts an item at the specified index:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:79:83"
    ```

## Add List Items
### Append Items
To add an item to the end of the list, use the **append()** method:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:86:90"
    ```
### Insert Items
To insert a list item at a specified index, use the **insert()** method.The **insert()** method inserts an item at the specified index:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:92:97"
    ```

### Extend Items
To append elements from another list to the current list, use the **extend()** method.The elements will be added to the end of the list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:99:104"
    ```

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:106:110"
    ```
## Remove List Items
### Remove Specified Item
The **remove()** method removes the specified item.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:113:117"
    ```

If there are more than one item with the specified value, the **remove()** method removes the first occurrence:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:119:123"
    ```

### Remove Specified Index
The **pop()** method removes the specified index.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:125:129"
    ```

If you do not specify the index, the **pop()** method removes the last item.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:131:135"
    ```

The **del** keyword also removes the specified index:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:137:141"
    ```

The **del** keyword can also delete the list completely.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:143:146"
    ```

### Clear the List
The **clear()** method empties the list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:148:152"
    ```

## Loop Lists
### Loop Through a List
You can loop through the list items by using a **for** loop:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:155:160"
    ```

### Loop Through the Index Numbers
You can iterate through the list items by accessing them using their index.To achieve this, use the **range()** function along with **len()** to generate the necessary indices.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:162:167"
    ```

### Using a While Loop
In Jac, you can iterate through list items using a **while** loop by leveraging the **len()** function.Start with an index of **0**, then loop through the list using its index until you reach the list's length. Ensure you increment the index in each iteration to avoid an infinite loop.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:169:176"
    ```

### Looping Using List Comprehension
List Comprehension offers the shortest syntax for looping through lists:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:178:181"
    ```
## Sort Lists
### Sort List Alphanumerically
List objects have a **sort()** method that will sort the list alphanumerically, ascending, by default:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:184:188"
    ```

### Sort Descending
To sort descending, use the keyword argument **reverse = True**:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:190:194"
    ```

### Customize Sort Function
You can define a custom function for sorting by using the keyword argument **key=function**.This function should return a numeric value, which will be used to determine the sorting order, with the lowest values appearing first.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:196:204"
    ```

### Case Insensitive Sort
By default the **sort()** method is case sensitive, resulting in all capital letters being sorted before lower case letters:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:206:210"
    ```

### Reverse Order
The **reverse()** method reverses the current sorting order of the elements:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:212:216"
    ```
## Copy Lists
You cannot copy a list simply by typing **list2 = list1**, because: **list2** will only be a reference to **list1**, and changes made in **list1** will automatically also be made in **list2**.

### Use the copy( ) method
You can use the built-in List method **copy()** to copy a list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:219:223"
    ```

### Use the slice Operator
You can also make a copy of a list by using the **:** (slice) operator.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:225:229"
    ```
## Join Lists
### Join Two Lists
In Jac, you can merge multiple lists in various ways, with the **+** operator being one of the simplest methods.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:232:238"
    ```

Or you can use the **extend()** method, where the purpose is to add elements from one list to another list:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list.jac:240:246"
    ```