## Strings
Strings in Jaclang are surrounded by either single quotation marks, or double quotation marks.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:1:4"
    ```

## Quotes Inside Quotes
You can use quotes inside a string, as long as they don't match the quotes surrounding the string:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:6:10"
    ```

## Multiline Strings
You can assign a multiline string to a variable by using three quotes:

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:12:16"
    ```

## Strings are Arrays
Like many other popular programming languages, strings in **JacLang** are sequences of characters used to represent text.  However, **JacLang** does not have a separate character data type; a single character is simply a string of length 1.Square brackets `[ ]` can be used to access individual characters within a string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:18:21"
    ```

## Looping Through a String
Since strings are arrays, we can loop through the characters in a string, with a **for** loop.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:23:27"
    ```

## String Length
To get the length of a string, use the **len()** function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:29:32"
    ```

## Check String
To check if a certain phrase or character is present in a string, we can use the keyword **in**.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings/intro/jac_strings_intro.jac:34:39"
    ```