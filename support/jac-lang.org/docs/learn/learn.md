# Jac Coding Manual

Jac is all of pythons goodness wrapped in a language that gives the coder wings. Lets jump right in!

## Get Jac

Install Jac.

```bash
pip install jaclang
```

Validate Jac works.

```bash
echo "with entry { print('hello world'); }" > test.jac;
jac run test.jac;
rm test.jac;"
```

If that command prints `hello world`, Jac is working.

Ok now lets jump into learning Jac!
## A Complete Example

We start this journey top down. Lets look at a simple but complete program in Python and two Jac versions. The first implements the module with very close resemblence to Python, and the second is the clean Jactastic way of implemmenting the same functionality. Lets look at the complete examples, then break it down.

=== "Python (circle.py)"
    ```python linenums="1"
    --8<-- "examples/manual_code/circle.py"
    ```
=== "Jac (circle.jac)"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle.jac"
    ```
=== "circle_clean.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle_clean.jac"
    ```
=== "circle_clean_impl.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle_clean_impl.jac"
    ```

Now lets break it down!

### Docstrings, Imports, and Globals

=== "circle.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle.jac::8"
    ```
=== "circle.py"
    ```python linenums="1"
    --8<-- "examples/manual_code/circle.py::11"
    ```

In this segment we observe a docstring, imports, and a global variable. In Jac docstrings look exactly like python docstrings, however docstrings can only be used as docstrings (not as comments). That means there are a limited number of places you can place them, these places are at the top of a module, and *before* the declaration of functions, methods, classes (architypes), global variable statements, module level code blocks (i.e., `with entry {}` style blocks, more on this later), and enumerations.

Import statements are very similar to python, note that you have to denote if you are importing a python module with `import:py` or jac with `import:jac`. Module paths and such are pretty much identical.

Quick note on from import, they work like this.

=== "Jac"
    ```jac
    import:py from os, getcwd, listdir, path
    ```
=== "Python"
    ```python
    from os import getcwd, listdir, path
    ```

The rationale for this change is purely aesthetic as when reading a file with many imports it looks good to have all the import keywords at the beginning.

### Abilities (Functions)

=== "circle.jac"
    ```jac linenums="10"
    --8<-- "examples/manual_code/circle.jac:10:13"
    ```
=== "circle.py"
    ```python linenums="13"
    --8<-- "examples/manual_code/circle.py:14:16"
    ```

A nomenclature introduced with  Jac is to refer to functions (and the soon described data spatial code blocks) as abilities. More on data spatial programming later, but for this example the functions in python and jac are very similar except the `def` keyword is replaced with `can.` Also type-hints are manditory in Jac for function signatures (parameters and returns). Any function that doesn't include it's return signature (i.e., `-> TYPE`) is implicitly assumed to be `-> None`.

Also note that the docstring appears *before* the function call. This choice was made for readability (function signatures closer to the code is better for code readability when a large docstring is used).

### Multiline Comments

=== "circle.jac"
    ```jac linenums="15"
    --8<-- "examples/manual_code/circle.jac:15:18"
    ```
=== "circle.py"
    ```python linenums="18"
    --8<-- "examples/manual_code/circle.py:19:23"
    ```

As Jac does not allow docstrings to be used as comments, Jac provides an elegant way to specify multiline comments. Any text between `#*` and `*#` is treated as a multi line comment (and is delightfully pythontic).

### Enumeration

=== "circle.jac"
    ```jac linenums="20"
    --8<-- "examples/manual_code/circle.jac:20:24"
    ```
=== "circle.py"
    ```python linenums="25"
    --8<-- "examples/manual_code/circle.py:26:30"
    ```

Jac includes enums as a language feature, the semantics of this enum is simple currently however will evolve over time. Of course you can import Enum to leverage pythons path if needed. However its important to note you'll have to use Jac's keyword escape feature to avoid a syntax error when referring to the enum package.

```jac
import:py from enum, Enum, auto;
```
If you try to import from enum this way in jac, you'll get a syntax error.


```jac
import:py from <>enum, Enum, auto;
```
This is the way to import from enum. Any language level keyword can be escaped by putting a `<>` immediately before the keyword.

### Shape Class

=== "circle.jac"
    ```jac linenums="26"
    --8<-- "examples/manual_code/circle.jac:26:32"
    ```
=== "circle.py"
    ```python linenums="32"
    --8<-- "examples/manual_code/circle.py:33:42"
    ```

This is an example of a Shape class in Jac. A couple things to note here.

### Circle Class

=== "circle.jac"
    ```jac linenums="34"
    --8<-- "examples/manual_code/circle.jac:34:45"
    ```
=== "circle.py"
    ```python linenums="43"
    --8<-- "examples/manual_code/circle.py:45:54"
    ```

### Script handling

=== "circle.jac"
    ```jac linenums="47"
    --8<-- "examples/manual_code/circle.jac:47:53"
    ```
=== "circle.py"
    ```python linenums="55"
    --8<-- "examples/manual_code/circle.py:57:65"
    ```

### Tests

=== "circle.jac"
    ```jac linenums="55"
    --8<-- "examples/manual_code/circle.jac:55:59"
    ```
=== "circle.py"
    ```python linenums="66"
    --8<-- "examples/manual_code/circle.py:68:81"
    ```

### Clean Approach

=== "circle_clean.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle_clean.jac"
    ```
=== "circle_clean_impl.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle_clean_impl.jac"
    ```
=== "circle.py"
    ```python linenums="1"
    --8<-- "examples/manual_code/circle.py"
    ```


## Complete list of Differences and Features beyond Python

Jac is a superset of Python 3, all of pythons features and full native compatability is present. However, each of the features  and adjustments described here represents Jac's approach to improve programmer effectiveness in a way that is distinct from Python. These choices were made focusing on type safety, readability, expressiveness, and general code ninja goodness. As the Jac language evolves, these features will be refined and expanded based on user feedback, practical usage, and the evolution of python and coding in general.

Additionally, Jac is the first language to implement the data spatial object paradigm. After getting used to Jac, we encourage every coder to expand their toolkit with this powerful programming model.

### Whitespace doesn't matter
Unlike Python, where indentation is crucial for defining code blocks, Jac does not consider whitespace for this purpose. This gives programmers more flexibility in formatting their code, although maintaining a consistent style is still recommended for readability. With more flexibility in how code can be laid out, more beautiful formatting styles are possible.

### Types hints are required
In Jac, type hints are mandatory for certain variable declarations and function signatures. This enforces type safety and makes the code more self-documenting, aiding in debugging and maintaining the codebase.

### Typing library implicitly available
Jac has a built-in typing system, similar to Python's typing library, but it's implicitly available. This means you don't need to import typing modules explicitly to use features like `List`, `Dict`, `Optional`, etc. You can simply reference them with a backtick as  `` `List ``, `` `Dict ``, and `` `Optional ``.

### Can separate definitions from declarations
In Jac, you can declare a function or a variable without defining it immediately. This separation allows for more organized code and makes it easier to manage large codebases with multiple dependencies.

### Tuples are explicit
Tuples in Jac must be explicitly declared, which differs from Python's implicit tuple creation. This design choice avoids accidental creation of tuples, enhancing code clarity.

### Docstrings in the right place
Docstrings in Jac are placed differently compared to Python. This change is aimed at improving readability and making the documentation process more intuitive and consistent.

### Elvis Operator
Jac introduces the Elvis operator (`?:`), which is a shorthand for an if-else statement, similar to the ternary operator in other languages. It provides a more concise way to write conditional expressions.

### Null Safe Operator
The Null Safe operator in Jac allows safe access to an object's properties or methods without the risk of encountering a null reference error. This operator helps in writing cleaner, more robust code.

### Filter Comprehension
Filter comprehension in Jac is a built-in feature that provides a more intuitive and concise way to filter collections, similar to list comprehensions in Python but with a focus on filtering.

### Assign Comprehension
Assign comprehension is a unique feature in Jac that allows for direct assignment within a comprehension, making certain patterns of data processing more succinct and readable.

### Dataclass style basis for OOP
Jac's approach to object-oriented programming is based on a dataclass style, where classes are primarily used to store data. This makes data handling more straightforward and efficient.

### Proper multiline Comments
Multiline comments in Jac are more versatile and user-friendly compared to Python. This feature enhances the ability to document code extensively without resorting to string literals or consecutive single-line comments.

### Explicit notation for special variables
Special variables in Jac have explicit notations, making it clear when such variables are being used. This feature aids in code readability and helps avoid accidental misuse of these variables.

### No need for gratuitous self usage
In Jac, there is no need to use the `self` keyword in all class method signatures as in Python. This design choice simplifies method definitions and makes the code cleaner and easier to read.

### Optional Left to right Pipe style expressivity
Jac offers an optional left-to-right pipe-style syntax for function calls, similar to the Unix pipeline or functional programming languages. This feature allows for more expressive and readable code, especially when chaining multiple function calls.

### Full Support of Data Spatial Programming Paradigmn
More on this soon!!!