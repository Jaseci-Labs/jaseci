## F-Strings
To specify a string as an f-string, simply put an **f** in front of the string literal, and add curly brackets **{ }** as placeholders for variables and other operations.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/format_strings/jac_f_string.jac:1:5"
    ```

## Placeholders and Modifiers
A placeholder can contain variables, operations, functions, and modifiers to format the value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/format_strings/jac_f_string.jac:7:11"
    ```

A placeholder can contain Jaclang code, like math operations:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/format_strings/jac_f_string.jac:13:16"
    ```

