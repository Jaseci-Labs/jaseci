## Loop Through a Dictionary
You can loop through a dictionary by using a for loop.When looping through a dictionary, the return value are the keys of the dictionary, but there are methods to return the values as well.

Print all key names in the dictionary, one by one:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/loop_dictionary/jac_loop_through_dict.jac:1:6"
    ```

Print all values in the dictionary, one by one:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/loop_dictionary/jac_loop_through_dict.jac:8:13"
    ```

You can also use the **values()** method to return values of a dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/loop_dictionary/jac_loop_through_dict.jac:15:20"
    ```

You can use the **keys()** method to return the keys of a dictionary:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/loop_dictionary/jac_loop_through_dict.jac:22:27"
    ```

Loop through both keys and values, by using the **items()** method:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/loop_dictionary/jac_loop_through_dict.jac:29:34"
    ```