## Change Tuple Values
Once a tuple is created, you cannot change its values. Tuples are **unchangeable**, or **immutable** as it also is called.But there is a workaround. You can convert the tuple into a list, change the list, and convert the list back into a tuple.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_update_tuple/jac_change_tuple.jac"
    ```

## Add Items
Since tuples are immutable, they do not have a built-in **append()** method, but there are other ways to add items to a tuple.

**1. Convert into a list:**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_update_tuple/jac_update_add_items.jac"
    ```

**2. Add tuple to a tuple:**

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_update_tuple/jac_update_tuple_2.jac"
    ```

## Remove Items
Tuples are **unchangeable**, so you cannot remove items from it, but you can use the same workaround as we used for changing and adding tuple items:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_update_tuple/jac_update_remove_items.jac"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_update_tuple/jac_update_tuple_del.jac"
    ```