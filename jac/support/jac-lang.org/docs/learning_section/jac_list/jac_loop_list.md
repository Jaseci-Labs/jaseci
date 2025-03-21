## Loop Through a List
You can loop through the list items by using a **for** loop:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Loop_list/jac_loop_list.jac:1:6"
    ```

## Loop Through the Index Numbers
You can iterate through the list items by accessing them using their index.To achieve this, use the **range()** function along with **len()** to generate the necessary indices.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Loop_list/jac_loop_list.jac:8:13"
    ```

## Using a While Loop
In Jac, you can iterate through list items using a **while** loop by leveraging the **len()** function.Start with an index of **0**, then loop through the list using its index until you reach the list's length. Ensure you increment the index in each iteration to avoid an infinite loop.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Loop_list/jac_loop_list.jac:15:22"
    ```

## Looping Using List Comprehension
List Comprehension offers the shortest syntax for looping through lists:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Loop_list/jac_loop_list.jac:24:27"
    ```