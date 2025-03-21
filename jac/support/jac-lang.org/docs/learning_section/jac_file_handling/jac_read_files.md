In JacLang, you can read files fully or partially using the read() and readline() methods. It is also best practice to close files after use.

## Reading Partial Content

To read only a specific number of characters from a file:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_read_file.jac:1:5"
    ```

## Reading a Single Line

Use **readline()** to return one line at a time:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_read_file.jac:7:11"
    ```

## Reading Multiple Lines

Calling **readline()** multiple times reads consecutive lines:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_read_file.jac:13:18"
    ```

## Reading the Whole File Line by Line

Using a loop to iterate through each line:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_read_file.jac:20:26"
    ```

## Closing Files
It's good practice to close a file after use:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_read_file.jac:28:33"
    ```