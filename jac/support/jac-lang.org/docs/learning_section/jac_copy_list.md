You cannot copy a list simply by typing **list2 = list1**, because: **list2** will only be a reference to **list1**, and changes made in **list1** will automatically also be made in **list2**.

## Use the copy( ) method
You can use the built-in List method **copy()** to copy a list.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Copy_list/jac_copy_method.jac:1:5"
    ```

## Use the slice Operator
You can also make a copy of a list by using the **:** (slice) operator.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Copy_list/jac_copy_method.jac:7:11"
    ```