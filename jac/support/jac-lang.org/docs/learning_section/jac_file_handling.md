JacLang provides a function similar to Python's open() to manage file operations. It supports multiple modes for handling files:

- `r` (Read) → Opens a file for reading (error if the file does not exist).
- `a` (Append) → Opens a file for appending (creates the file if it does not exist).
- `w` (Write) → Opens a file for writing (creates the file if it does not exist).
- `x` (Create) → Creates a new file (error if the file already exists).

Additionally, files can be opened in.

- `t` (Text Mode) → Default mode for reading/writing text.
- `b` (Binary Mode) → Used for handling binary files like images.

## Syntax Example

To open a file for reading.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:2:6"
    ```

Equivalent to.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:8:12"
    ```

## Read Files

In JacLang, you can read files fully or partially using the **read()** and **readline()** methods. It is also best practice to close files after use.

### Reading Partial Content

To read only a specific number of characters from a file.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:15:20"
    ```

### Reading a Single Line

Use **readline()** to return one line at a time.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:21:26"
    ```

### Reading Multiple Lines

Calling **readline()** multiple times reads consecutive lines.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:27:33"
    ```

### Reading the Whole File Line by Line

Using a loop to iterate through each line.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:34:41"
    ```

### Closing Files
It's good practice to close a file after use.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:42:49"
    ```

## Write/Create Files

In JacLang, you can write, append, and create files using different modes in the **open()** function.

Writing to an Existing File to write or append to an existing file, specify a mode.

- `a` → Append (adds content to the end of the file).
- `w` → Write (overwrites the entire file).

**Appending to a File**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:52:56"
    ```

**Overwriting a File**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:58:62"
    ```

### Creating a New File

You can create new files using.

- `x` → Create (creates a new file, error if it already exists).
- `a` or `w` → Creates the file if it does not exist.

**Creating a File Using "x" Mode**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:66:75"
    ```

**Creating a File Using "w" Mode**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:77:86"
    ```

## Delete Files

To delete a file, you must import the OS module, and run its **os.remove()** function.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:90:99"
    ```

To delete a folder, you must import the OS module, and run its **os.rmdir()** function.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling.jac:101:110"
    ```
