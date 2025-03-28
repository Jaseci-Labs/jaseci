- The **try** block lets you test a block of code for errors.

- The **except** block lets you handle the error.

- The **else** block lets you execute code when there is no error.

- The **finally** block lets you execute code, regardless of the result of the try- and except blocks.

## Exception Handling

When an error occurs, or an exception as we call it, Jac will normally stop and generate an error message.These exceptions can be handled using the try statement.Since the try block raises an error, the except block will be executed.Without the try block, the program will crash and raise an error.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_try_except/jac_try_except.jac:1:7"
    ```

## Else

You can use the else keyword to define a block of code to be executed if no errors were raised:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_try_except/jac_try_except.jac:9:17"
    ```

## Finally

The **finally** block, if specified, will be executed regardless if the try block raises an error or not.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_try_except/jac_try_except.jac:19:27"
    ```

## Raise an exception

You can choose to raise an exception when a condition occurs.To **raise** an exception, use the **raise** statement.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_try_except/jac_try_except.jac:29:41"
    ```