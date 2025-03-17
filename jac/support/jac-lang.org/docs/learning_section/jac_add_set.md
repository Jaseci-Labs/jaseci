## Add Items
**1.Using Add( ) method**

To add one item to a set use the **add()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_add_item/jac_sets_add_items.jac"
    ```

**2.Using update( ) method**

To add items from another set into the current set, use the **update()** method.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_add_item/jac_sets_update.jac"
    ```

## Add Any Iterable

The object in the **update()** method does not have to be a set, it can be any iterable object (tuples, lists, dictionaries etc.).

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_add_item/jac_add_iterable.jac"
    ```