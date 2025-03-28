## Remove Specified Item
The **remove()** method removes the specified item.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:1:5"
    ```

If there are more than one item with the specified value, the **remove()** method removes the first occurrence:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:7:11"
    ```

## Remove Specified Index
The **pop()** method removes the specified index.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:13:17"
    ```

If you do not specify the index, the **pop()** method removes the last item.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:19:23"
    ```

The **del** keyword also removes the specified index:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:25:29"
    ```

The **del** keyword can also delete the list completely.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:31:34"
    ```

## Clear the List
The **clear()** method empties the list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Remove_list_items/jac_remove_1.jac:36:40"
    ```
