In JacLang, you can write, append, and create files using different modes in the **open()** function.

Writing to an Existing File
To write or append to an existing file, specify a mode:

- "a" → Append (adds content to the end of the file).
- "w" → Write (overwrites the entire file).

**Appending to a File**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_create_file.jac:1:5"
    ```

**Overwriting a File**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_create_file.jac:7:11"
    ```

## Creating a New File

You can create new files using:

- "x" → Create (creates a new file, error if it already exists).
- "a" or "w" → Creates the file if it does not exist.

**Creating a File Using "x" Mode**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_write_file.jac:1:10"
    ```

**Creating a File Using "w" Mode**

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_write_file.jac:12:21"
    ```
