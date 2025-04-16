## Introduction

### Basic Structure
Strings in Jaclang are surrounded by either single quotation marks, or double quotation marks.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:2:5"
    ```

### Quotes Inside Quotes
You can use quotes inside a string, as long as they don't match the quotes surrounding the string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:7:11"
    ```

### Multiline Strings
You can assign a multiline string to a variable by using three quotes.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:13:17"
    ```

### Strings are Arrays
Like many other popular programming languages, strings in **JacLang** are sequences of characters used to represent text. However, **JacLang** does not have a separate character data type; a single character is simply a string of length one. Square brackets [ ] can be used to access individual characters within a string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:19:22"
    ```

### Looping Through a String
Since strings are arrays, we can loop through the characters in a string, with a **for** loop.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:24:28"
    ```

### String Length
To get the length of a string, use the **len()** function.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:30:34"
    ```

### Check String
To check if a certain phrase or character is present in a string, we can use the keyword **in**.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:35:40"
    ```

## Slicing
You can return a range of characters by using the slice syntax. Specify the start index and the end index, separated by a colon, to return a part of the string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:44:47"
    ```

### Slice From the Start
By leaving out the start index, the range will start at the first character.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:49:52"
    ```

### Slice To the End
By leaving out the end index, the range will go to the end.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:54:57"
    ```
## Modify Strings

### Upper Case
The **upper( )** method returns the string in upper case.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:61:64"
    ```

### Lower Case
The **lower( )** method returns the string in lower case.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:66:69"
    ```

### Remove Whitespace
Whitespace refers to the space before and/or after the actual text, and very often, you may want to remove this space. The **strip()** method removes any leading and trailing whitespace by default.

If needed, you can also specify which characters to remove by passing them as an argument to **strip()**.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:71:74"
    ```

### Replace String
The **replace( )** method replaces a string with another string.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:76:79"
    ```

### Split String
The **split( )** method returns a list where the text between the specified separator becomes the list items.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:81:84"
    ```

## String Concatenation
To concatenate, or combine, two strings you can use the **+** operator.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:88:93"
    ```

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:95:100"
    ```

## Format Strings

### F-Strings
To specify a string as an f-string, simply put an **f** in front of the string literal, and add curly brackets **{ }** as placeholders for variables and other operations.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:104:108"
    ```

### Placeholders and Modifiers
A placeholder can contain variables, operations, functions, and modifiers to format the value.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:110:114"
    ```

A placeholder can contain Jaclang code, like math operations.

**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_strings.jac:116:119"
    ```

