- to explain Jac code.
- to make the code more readable.
- to prevent execution when testing code.

## Creating a Comment
Comments starts with a `#`, and Jac will ignore them:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:1:4"
    ```
**Code Example**
In JacLang, an inline comment starts with `#` and is used to add brief explanations within the code.

=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:6:8"
    ```
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:10:13"
    ```

## Multiline Comments
Jac does not really have a syntax for multiline comments.To add a multiline comment you could insert a `#` for each line:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:15:20"
    ```
**Code Example**
A multiline string in JacLang is enclosed within triple quotes (`"""` or `'''`) and allows storing text across multiple lines while preserving formatting.

=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:22:29"
    ```