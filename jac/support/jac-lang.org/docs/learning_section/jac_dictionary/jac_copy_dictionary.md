## Copy a Dictionary

You cannot copy a dictionary simply by typing `dict2 = dict1`, because: `dict2` will only be a reference to `dict1`, and changes made in `dict1` will automatically also be made in `dict2`.

There are ways to make a copy, one way is to use the built-in Dictionary method **copy()**.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/copy_dict/jac_copy_dict.jac:1:5"
    ```

Another way to make a copy is to use the built-in function `dict()`.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/copy_dict/jac_copy_dict.jac:7:11"
    ```