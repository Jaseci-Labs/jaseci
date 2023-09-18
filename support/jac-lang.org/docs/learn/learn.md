# Coding Manual

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
## Modules in Jac

We start this journey top down. Lets look at a simple but complete program in python and the Jac version.

=== "Jac (circle.jac)"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle.jac"
    ```
=== "Python (circle.py)"
    ```python linenums="1"
    --8<-- "examples/manual_code/circle.py"
    ```

Now lets break it down!

### Docstrings, Imports, and Globals

=== "circle.jac"
    ```jac linenums="1"
    --8<-- "examples/manual_code/circle.jac::8"
    ```
=== "circle.py"
    ```python linenums="1"
    --8<-- "examples/manual_code/circle.py::10"
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

### Functions / Abilities

=== "circle.jac"
    ```jac linenums="10"
    --8<-- "examples/manual_code/circle.jac:10:13"
    ```
=== "circle.py"
    ```python linenums="13"
    --8<-- "examples/manual_code/circle.py:13:15"
    ```

A nomenclature in Jac is to refer to functions and data spatial code blocks as types of abilities. More on data spatial programming later, but for this example the functions in python and jac are very similar except the `def` keyword is replaced with `can.` Also type-hints are manditory in Jac for function signatures (parameters and returns). Any function that doesn't include it's return signature (i.e., `-> TYPE`) is implicitly assumed to be `-> None`.

Also note that the docstring appears *before* the function call. This choice was made for readability (function signatures closer to the code is better for code readability when a large docstring is used).

### Multiline Comments

=== "circle.jac"
    ```jac linenums="15"
    --8<-- "examples/manual_code/circle.jac:15:18"
    ```
=== "circle.py"
    ```python linenums="18"
    --8<-- "examples/manual_code/circle.py:18:22"
    ```

As Jac does not allow docstrings to be used as comments, Jac provides an elegant way to specify multiline comments. Any text between `#*` and `*#` is treated as a multi line comment (and is delightfully pythontic).

### Enumeration

=== "circle.jac"
    ```jac linenums="20"
    --8<-- "examples/manual_code/circle.jac:20:24"
    ```
=== "circle.py"
    ```python linenums="25"
    --8<-- "examples/manual_code/circle.py:25:29"
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
    --8<-- "examples/manual_code/circle.py:32:40"
    ```

This is an example of a Shape class in Jac. A couple things to note here.

### Circle Class

=== "circle.jac"
    ```jac linenums="34"
    --8<-- "examples/manual_code/circle.jac:34:45"
    ```
=== "circle.py"
    ```python linenums="43"
    --8<-- "examples/manual_code/circle.py:43:52"
    ```

### Script handling

=== "circle.jac"
    ```jac linenums="47"
    --8<-- "examples/manual_code/circle.jac:47:53"
    ```
=== "circle.py"
    ```python linenums="55"
    --8<-- "examples/manual_code/circle.py:55:63"
    ```

### Tests

=== "circle.jac"
    ```jac linenums="55"
    --8<-- "examples/manual_code/circle.jac:55:59"
    ```
=== "circle.py"
    ```python linenums="66"
    --8<-- "examples/manual_code/circle.py:66:79"
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