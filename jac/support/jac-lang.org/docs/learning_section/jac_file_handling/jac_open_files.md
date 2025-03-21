JacLang provides a function similar to Python's open() to manage file operations. It supports multiple modes for handling files:

- "r" (Read) → Opens a file for reading (error if the file does not exist).
- "a" (Append) → Opens a file for appending (creates the file if it does not exist).
- "w" (Write) → Opens a file for writing (creates the file if it does not exist).
- "x" (Create) → Creates a new file (error if the file already exists).

Additionally, files can be opened in:

- "t" (Text Mode) → Default mode for reading/writing text.
- "b" (Binary Mode) → Used for handling binary files like images.
Syntax Example
To open a file for reading:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_open_file.jac:1:5"
    ```

Equivalent to:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_file_handling/jac_open_file.jac:7:11"
    ```
