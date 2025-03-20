## Access Tuple Items
You can access tuple items by referring to the index number, inside square brackets:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_tuple_access/jac_access_tuple_items.jac:1:4"
    ```

## Negative Indexing
Negative indexing means start from the end.**-1** refers to the last item, **-2** refers to the second last item etc.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_tuple_access/jac_access_tuple_items.jac:6:9"
    ```

## Range of Indexes
You can specify a range of indexes by specifying where to start and where to end the range.When specifying a range, the return value will be a new tuple with the specified items.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_tuple_access/jac_access_tuple_items.jac:11:14"
    ```
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_tuple_access/jac_access_tuple_items.jac:16:19"
    ```

## Check if Item Exists
To determine if a specified item is present in a tuple use the **in** keyword:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_tuple/jac_tuple_access/jac_access_tuple_items.jac:21:25"
    ```