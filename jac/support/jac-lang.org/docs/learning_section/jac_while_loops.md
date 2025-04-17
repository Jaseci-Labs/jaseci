A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).

This is less like the for keyword in other programming languages, and works more like an iterator method as found in other object-orientated programming languages.

## Basic While loop
With the while loop we can execute a set of statements as long as a condition is true.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_while_loop.jac:1:7"
    ```

## While True

Jac supports infinite loops using `while True`, which can be useful in scenarios where you want a loop to run continuously until a break condition is met from inside the loop.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_while_loop.jac:31:40"
    ```

- In this example, the loop will keep running indefinitely unless the `break` statement is triggered when `i > 5`.

## While is not

Jac allows expressive comparison using `is not`, which can be used in `while` loops to check if a variable does **not** match a specific value.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_while_loop.jac:42:48"
    ```

## Break Statement
With the **break** statement we can stop the loop even if the while condition is true.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_while_loop.jac:9:18"
    ```

## Continue Statement
With the **continue** statement we can stop the current iteration, and continue with the next.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_while_loop.jac:20:29"
    ```
