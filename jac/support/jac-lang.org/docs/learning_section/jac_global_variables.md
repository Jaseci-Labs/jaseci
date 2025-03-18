## Global Variables
In **JacLang**, variables created outside of a function are known as **global variables**.Global variables are accessible from anywhere in the code, both inside functions and outside of them.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables/global_variables/jac_variables_1.jac"
    ```

If you create a variable with the same name inside a function, this variable will be local, and can only be used inside the function. The global variable with the same name will remain as it was, global and with the original value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables/global_variables/jac_variables_2.jac"
    ```

## The Global Keyword
Normally, when you create a variable inside a function, that variable is local, and can only be used inside that function.To create a global variable inside a function, you can use the **global** keyword.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables/global_variables/jac_variables_glob_1.jac"
    ```

Also, use the global keyword if you want to change a global variable inside a function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_variables/global_variables/jac_variables_glob_2.jac"
    ```
