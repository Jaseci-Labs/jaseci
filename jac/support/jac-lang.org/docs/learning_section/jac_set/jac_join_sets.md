## Join Sets

There are several ways to join two or more sets in Python.

- The union( ) and update( ) methods joins all items from both sets.
- The intersection( ) method keeps ONLY the duplicates.
- The difference( ) method keeps the items from the first set that are not in the other set(s).
- The symmetric_difference( ) method keeps all items EXCEPT the duplicates.

## Union

The **union()** method returns a new set with all items from both sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:1:7"
    ```

You can use the **|** operator instead of the **union()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:9:15"
    ```

## Join Multiple Sets

All the joining methods and operators can be used to join multiple sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:17:25"
    ```

When using the | operator, separate the sets with more | operators:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:27:35"
    ```

## Update

The update() method inserts all items from one set into another.The update() changes the original set, and does not return a new set.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:37:43"
    ```

## Intersection

The intersection() method will return a new set, that only contains the items that are present in both sets.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:45:51"
    ```
You can use the **&** operator instead of the **intersection()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:53:59"
    ```

## Difference

The **difference()** method will return a new set that will contain only the items from the first set that are not present in the other set.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:61:68"
    ```

You can use the **-** operator instead of the **difference()** method, and you will get the same result.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_sets/jac_sets_join/jac_join_set.jac:70:77"
    ```