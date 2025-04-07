## Introduction
Variables are containers for storing data values.

### Basic structure
Jaclang has no command for declaring a variable. A variable is created the moment you first assign a value to it.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:2:8"
    ```

### Casting
If you want to specify the data type of a variable, this can be done with casting.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:9:17"
    ```

### Get the Type
You can get the data type of a variable with the **type()** function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:18:24"
    ```

### Case-Sensitive
Variable names are case-sensitive.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:25:31"
    ```

## Variable Names
- A variable name must start with a letter or the underscore character (_).
- A variable name cannot start with a number.
- A variable name can only contain alphanumeric characters (A-Z, 0-9) and underscores (_).
- Variable names are case-sensitive (e.g., age, Age, and AGE are considered different variables).
- A variable name cannot be a reserved keyword in JacLang.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:33:41"
    ```

### Multi Words Variable Names
Variable names with more than one word can be difficult to read.There are several techniques you can use to make them more readable.

- **Camel Case :**
Each word, except the first, starts with a capital letter. `myVariableName = "John"`

- **Pascal Case :**
Each word starts with a capital letter. `MyVariableName = "John"`

- **Snake Case :**
Each word is separated by an underscore character. `my_variable_name = "John"`

## Output Variables
The Jaclang `print()` function is often used to output variables.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:43:48"
    ```
In the `print()` function, you output multiple variables, separated by a comma.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:48:54"
    ```
## Global Variables
In **JacLang**, variables created outside of a function are known as **global variables**.Global variables are accessible from anywhere in the code, both inside functions and outside of them.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:56:63"
    ```

If you create a variable with the same name inside a function, this variable will be local, and can only be used inside the function. The global variable with the same name will remain as it was, global and with the original value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:64:74"
    ```

### The Global Keyword
In JacLang, a variable created inside a function is local by default, but can be made global using the `global` keyword.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:75:83"
    ```

Also, use the global keyword if you want to change a global variable inside a function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables.jac:84:95"
    ```
