# Access Tags in Jac

In Jac, **Access Tags** control the visibility and accessibility of various elements like,

- architypes
- attributes (`has`)
- abilities (`can`)
- enumerations (`enum`)
- global variables (`glob`)

By using these access tags, we can ensure proper encapsulation and prevent unintended access.


## Types of Access Tags

Jac provides three main access levels:

| Access Tag | Description |
|----------|----------|
| `pub`   | **(Public)** - Accessible from anywhere   |
| `protect`    | **(Protected)** - Accessible within the same scope and derived elements   |
| `priv`    | **(Private)** - Accessible only within the same scope   |

We'll explore each access tag in the following examples.

---

## Access Tags for Global Variables

Global variables in Jac can be restricted using access tags.

### Public Global Variables (`pub`)

If a global variable is marked with the `pub` access tag, it can be accessed anywhere—in the **same module** or in any module that **imports** it.

**Code Example:**

#### Defining a Public Global Variable

Let's say we define a global variable in one file:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:6:7"
```

- Since the global variable `num1` is marked with the `pub` access tag, it can be accessed from anywhere in the program, both within the same file or in other files that import `file1.jac`.


#### Accessing the Public Global Variable

Now, let's see how we can access the `num1` variable in the **same module** and from **other modules**.

**Example 1: Accessing Within the Same Module**

- You can access the `num1` global variable directly in the same module, like so:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:6:11"
```


**Example 2: Accessing from Another File**

- To access the global variable `num1` from another file, you simply need to **import** the module where num1 is defined.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:13:18"
```


### Private Global Variables (`priv`)

When a global variable is marked with the `priv` tag, it becomes **private** to the module where it is defined. This means it cannot be accessed from other modules, even if those modules import the file where the variable is defined.

**Code Example:**

#### Defining a Private Global Variable

Let's say you define a global variable in one file:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:22:23"
```

- Since the global variable `num2` is marked with the `priv` access tag, it can **only be accessed** in `file1.jac` and **not** in any other files that import `file1.jac`.

#### Accessing the Private Global Variable

**Example 1: Accessing Within the Same Module**

- You can access the `num2` global variable directly in the same module, like so:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:22:27"
```


**Example 2: Accessing from Another File**

- If you try to access the `num2` global variable from a different file, it will not work because `num2` is private to `file1.jac`.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag.jac:29:34"
```