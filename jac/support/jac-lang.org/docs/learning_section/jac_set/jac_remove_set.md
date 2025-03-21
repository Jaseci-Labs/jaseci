## Remove Item
To remove an item in a set, use the **remove()**, or the **discard()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_remove_item/jac_sets_remove.jac:1:5"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_remove_item/jac_sets_remove.jac:7:11"
    ```

You can also use the **pop()** method to remove an item, but this method will remove a random item, so you cannot be sure what item that gets removed.The return value of the **pop()** method is the removed item.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_remove_item/jac_sets_remove.jac:13:18"
    ```

The **clear()** method removes all items from a set, leaving it empty.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_remove_item/jac_sets_remove.jac:20:24"
    ```
The **del** keyword deletes a set entirely. After using **del**, the set no longer exists.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_remove_item/jac_sets_remove.jac:26:29"
    ```