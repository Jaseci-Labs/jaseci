## Basic Dictionary
Dictionaries are used to store data values in `key:value` pairs.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/intro/jac_intro_dictionary.jac:1:4"
    ```

## Dictionary Items
Dictionary items are ordered, changeable, and do not allow duplicates.Dictionary items are presented in `key:value` pairs, and can be referred to by using the key name.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/intro/jac_intro_dictionary.jac:6:9"
    ```

## Ordered
In JacLang, dictionaries are ordered, meaning key-value pairs retain their insertion order. This ensures predictable access and iteration over elements. Unlike lists, dictionary items cannot be accessed by index but must be referenced using their unique keys.

## Changeable

Dictionaries are changeable, meaning that we can change, add or remove items after the dictionary has been created.

## Duplicates Not Allowed

Dictionaries cannot have two items with the same key:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/intro/jac_intro_dictionary.jac:11:14"
    ```

## Dictionary Length

To determine how many items a dictionary has, use the `len()` function:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_dictionary/intro/jac_intro_dictionary.jac:16:19"
    ```
