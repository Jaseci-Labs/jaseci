## Strings
Strings in Jaclang are surrounded by either single quotation marks, or double quotation marks.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_string_basic.jac"
    ```

## Quotes Inside Quotes
You can use quotes inside a string, as long as they don't match the quotes surrounding the string:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_quote_inside_quotes.jac"
    ```

## Multiline Strings
You can assign a multiline string to a variable by using three quotes:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_multiline_strings.jac"
    ```

## Strings are Arrays
Like many other popular programming languages, strings in **JacLang** are sequences of characters used to represent text.  However, **JacLang** does not have a separate character data type; a single character is simply a string of length 1.Square brackets `[ ]` can be used to access individual characters within a string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_string_arrays.jac"
    ```

## Looping Through a String
Since strings are arrays, we can loop through the characters in a string, with a **for** loop.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_string_for_loop.jac"
    ```

## String Length
To get the length of a string, use the **len()** function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_string_len.jac"
    ```

## Check String
To check if a certain phrase or character is present in a string, we can use the keyword **in**.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_string_check.jac"
    ```