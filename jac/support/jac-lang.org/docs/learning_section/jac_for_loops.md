A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).

This is less like the for keyword in other programming languages, and works more like an iterator method as found in other object-orientated programming languages.

## Looping Through a List
With the for loop we can execute a set of statements, once for each item in a list, tuple, set etc.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_list.jac"
    ```

## Looping Through a String
Even strings are iterable objects, they contain a sequence of characters:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_string.jac"
    ```

## The break Statement
With the break statement we can stop the loop before it has looped through all the items:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_break.jac"
    ```
## The continue Statement
With the continue statement we can stop the current iteration of the loop, and continue with the next:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_continue.jac"
    ```

## Pass Statement
for loops cannot be empty, but if you for some reason have a for loop with no content, put in the pass statement to avoid getting an error.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_pass.jac"
    ```

## The range( ) Function
To loop through a set of code a specified number of times, we can use the range() function,
The range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and ends at a specified number:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_range_1.jac"
    ```
The range() function defaults to 0 as a starting value,however it is possible to specify the starting value by adding a parameter:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_range_2.jac"
    ```
The range() function defaults to increment the sequence by 1, however it is possible to specify the increment value by adding a third parameter:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_range_3.jac"
    ```
## Else in For Loop
The else keyword in a for loop specifies a block of code to be executed when the loop is finished:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_else.jac"
    ```
## Nested Loops
A nested loop is a loop inside a loop.The "inner loop" will be executed one time for each iteration of the "outer loop":

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_for_loop/jac_for_nested_loops.jac"
    ```