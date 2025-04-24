- To explain Jac code.
- To make the code more readable.
- To prevent execution when testing code.

## Creating a Comment
Comments starts with a `#`, and Jac will ignore them.

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

In Jaclang, to include comments across multiple lines in Jac, place the `#` symbol at the beginning of each line.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:15:20"
    ```
## Docstrings

**Code Example**

In JacLang, docstrings are (""" or ''') used to document code. They're not comments but actual string literals that describe nodes, functions, and more.

=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_comments.jac:22:29"
    ```