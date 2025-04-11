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
--8<-- "examples/learning_section/jac_access_tag_file1.jac:6:7"
```

- Since the global variable `num1` is marked with the `pub` access tag, it can be accessed from anywhere in the program, both within the same file or in other files that import `file1.jac`.


#### Accessing the Public Global Variable

Now, let's see how we can access the `num1` variable in the **same module** and from **other modules**.

**Example 1: Accessing Within the Same Module**

- You can access the `num1` global variable directly in the same module, like so:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:6:11"
```


**Example 2: Accessing from Another File**

- To access the global variable `num1` from another file, you simply need to **import** the module where num1 is defined.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file2.jac:3:7"
```


### Private Global Variables (`priv`)

When a global variable is marked with the `priv` tag, it becomes **private** to the module where it is defined. This means it cannot be accessed from other modules, even if those modules import the file where the variable is defined.

**Code Example:**

#### Defining a Private Global Variable

Let's say you define a global variable in one file:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:14:14"
```

- Since the global variable `num2` is marked with the `priv` access tag, it can **only be accessed** in `file1.jac` and **not** in any other files that import `file1.jac`.

#### Accessing the Private Global Variable

**Example 1: Accessing Within the Same Module**

- You can access the `num2` global variable directly in the same module, like so:

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:14:18"
```


**Example 2: Accessing from Another File**

- If you try to access the `num2` global variable from a different file, it will not work because `num2` is private to `file1.jac`.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file2.jac:10:13"
```


## Access Tags for Architypes

In Jac, architypes define with different access levels. The `:pub` (public), `:priv` (private), and `:protect` (protected) tags determine how these architypes can be accessed from different scopes.


### Public Architypes

An architype marked as `:pub` is accessible **from anywhere** in the program.

Other objects, entry functions, and external modules can **freely** reference and instantiate.

**Code Example**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:30:37"
```


### Private Architypes

If an Architype is marked as `:priv`, it cannot be accessed from outside its relavant scope.

**Code Example**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:41:48"
```

- In the above example `InnerPrivObj` Architype has been defined inside the Architype `SomeObj`. So, we can't create instances of `InnerPrivObj` outside the `SomeObj`'s scope.



## Access Tags for Attributes

In Jac, **attributes** can have different access levels to control how they are used and modified. These access levels help in **encapsulation** and **data security**.

### Public Attributes

A **public** attribute can be accessed and modified **from anywhere**.

**Code Example**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:59:67"
```

### Private Attributes

Let's say a **private** attribute is defined inside an Architype.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:70:72"
```

That **private** attribute **can be accessed or Modified** inside the Architype.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:74:84"
```

A **private** attribute **cannot be accessed or modified** outside the object. It is used to store internal data that should not be directly modified.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:86:94"
```

## Access Tags for Abilities

In Jac, **abilities** can have different access levels. These access levels define where an ability can be **called from**.

### Public Abilities

A **public** ability can be called from **anywhere** outside the object.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:98:107"
```

### Private Abilities

Let's say a **private** ability is defined inside an Architype.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:110:114"
```

That **private** ability **can be called** inside the Architype's scope.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:116:123"
```

A **private** ability **cannot be called** outside the Architype's scope.

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:125:133"
```

## Access Tags for Enums

In Jac, **enumerations (enum)** can have access tags to control their visibility across different modules. These access tags help ensure that enums are only accessible where needed, improving encapsulation and modularity.


### Public Enums

An enumeration marked as `pub` can be accessed **from anywhere**, including other modules that import it.

**Code Example: Defining a Public Enum**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:138:142"
```

**Code Example: Accessing from Another File**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file2.jac:17:19"
```

- Since `Color` is public, it can be accessed in `jac_access_tag_file2.jac` after importing `jac_access_tag_file1.jac`.


### Private Enums

An enumeration marked as `priv` **cannot be accessed outside** the module it is defined in.

**Code Example: Defining a Private Enum**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:150:158"
```

**Code Example: Attempting to Access from Another File**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file2.jac:22:25"
```

- Since `Color` is private, it **cannot be accessed in** `jac_access_tag_file2.jac`, even if `jac_access_tag_file1.jac` is imported.


### Protected Enum

An enumeration marked as `protect` is accessible within the same module and derived elements, but not from external files.


**Code Example: Defining a Protected Enum**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file1.jac:162:170"
```

**Code Example: Attempting to Access from Another File**

```jac linenums="1"
--8<-- "examples/learning_section/jac_access_tag_file2.jac:28:30"
```

- Since `Color` is protected, it **cannot be accessed** in `jac_access_tag_file2.jac`, even if `jac_access_tag_file1.jac` is imported.