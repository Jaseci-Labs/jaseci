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

### Functions / Abilities

=== "circle.jac"
    ```jac linenums="10"
    --8<-- "examples/manual_code/circle.jac:10:13"
    ```
=== "circle.py"
    ```python linenums="13"
    --8<-- "examples/manual_code/circle.py:13:15"
    ```

### Multiline Comments

=== "circle.jac"
    ```jac linenums="15"
    --8<-- "examples/manual_code/circle.jac:15:18"
    ```
=== "circle.py"
    ```python linenums="18"
    --8<-- "examples/manual_code/circle.py:18:22"
    ```

### Enumeration

=== "circle.jac"
    ```jac linenums="20"
    --8<-- "examples/manual_code/circle.jac:20:24"
    ```
=== "circle.py"
    ```python linenums="25"
    --8<-- "examples/manual_code/circle.py:25:29"
    ```

### Shape Class

=== "circle.jac"
    ```jac linenums="27"
    --8<-- "examples/manual_code/circle.jac:27:36"
    ```
=== "circle.py"
    ```python linenums="32"
    --8<-- "examples/manual_code/circle.py:32:40"
    ```

### Circle Class

=== "circle.jac"
    ```jac linenums="38"
    --8<-- "examples/manual_code/circle.jac:38:50"
    ```
=== "circle.py"
    ```python linenums="43"
    --8<-- "examples/manual_code/circle.py:43:52"
    ```

### Script handling

=== "circle.jac"
    ```jac linenums="52"
    --8<-- "examples/manual_code/circle.jac:52:58"
    ```
=== "circle.py"
    ```python linenums="55"
    --8<-- "examples/manual_code/circle.py:55:63"
    ```

### Tests

=== "circle.jac"
    ```jac linenums="60"
    --8<-- "examples/manual_code/circle.jac:60:64"
    ```
=== "circle.py"
    ```python linenums="66"
    --8<-- "examples/manual_code/circle.py:66:79"
    ```