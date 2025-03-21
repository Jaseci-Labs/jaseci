## Variable Names

- A variable name must start with a letter or the underscore character (_).
- A variable name cannot start with a number.
- A variable name can only contain alphanumeric characters (A-Z, 0-9) and underscores (_).
- Variable names are case-sensitive (e.g., age, Age, and AGE are considered different variables).
- A variable name cannot be a reserved keyword in LacLang.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables/variable_name/jac_variable_names.jac"
    ```

## Multi Words Variable Names
Variable names with more than one word can be difficult to read.There are several techniques you can use to make them more readable:

## Camel Case
Each word, except the first, starts with a capital letter:

`myVariableName = "John"`
## Pascal Case
Each word starts with a capital letter:

`MyVariableName = "John"`
## Snake Case
Each word is separated by an underscore character:

`my_variable_name = "John"`

