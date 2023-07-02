# A Tour of Jac

## Comments

Comments are parts of code ignored by the Jac compiler.

### Single Line Comments

In Jac, single line comments are the same as Python using the `#` symbol. Everything after `#` on the line is considered a comment.

Example:

```jac
# This is a single line comment
global x = 5;  # This comment is explaining this line of code
```

### Multi-line Comments

Python doesn't have a specific syntax for multi-line comments however Jac does! We extend upon Pythons `#` and base on inspiration of the C/C++/JS/TS `/*`, `*/` enclosures, we introduce `#*` and `*#` enclosures.

```jac
#* This is a multi-line comment since
it is made of two lines *#
```

## Doc Strings

Jac uses the same syntax for docstrings as Python, however Jac is more strict when it comes to using doc strings for comments. Given that Jac provides multiline comments, the need to hack doc strings to serve as comments is gone and in Jac doc strings should only be used for... doc strings (documentation documentation of functions, classes / architypes, and modules).

Docstrings are represented using triple quotes (`'''` or `"""`) in Jac, but please do not use them like this:

### Bad example
```Jac
'''
Do not use doc strings
for multi line comments.
'''
```

Indeed, the Jac compiler only allows Docstrings to be attached to the heads of modules, functions, classes / architypes, and methods. They appear right after the definition of a function, method, class, or module. You can use single, double, triple single or triple double quotes for docstrings.

### Good Example
In Python:

```python
def add(a, b):
    '''
    This function adds two numbers and returns the result.

    Parameters:
    a (int): The first number
    b (int): The second number

    Returns:
    int: The sum of the two numbers
    '''

    return a + b
```

In Jac:

```Jac
'''
This function adds two numbers and returns the result.

Parameters:
a: The first number
b: The second number

Returns: The sum of the two numbers
'''
can add(a: int, b: int) -> int {
    return a + b;
}
```

## Separable Defs / Decls

### Code

* Be sure to show both within a single file with sub defined functionality spec'd later

### Description