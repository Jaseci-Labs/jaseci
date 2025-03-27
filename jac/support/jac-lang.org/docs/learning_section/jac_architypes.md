## Architypes and Abilities

### What are Architypes?
In Jac, **Architypes** define the fundamental building blocks of a program. They describe different types of entities that interact within the system.


### Types of Architypes

Architypes define different types of entities in Jac, used for both **object-oriented** and **graph-based programming.**

- **`class`** - A **standard class** used for object-oriented programming. It defines reusable structures with attributes and methods.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:2:2"
    ```

- **`obj`** - Similar to class, but represents **single-instance objects** rather than reusable templates.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:4:4"
    ```

!!! note
    We need `node`, `edge` and `walker` Architypes specially for **Data Spatial Programming concept** in Jac.


- **`node`** - Represents a **node** in a graph-based structure. Nodes store data and are connected using edge architypes.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:6:6"
    ```

- **`edge`** - Defines the **connection** between two `node` architypes. Edges store relationships between nodes.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:8:8"
    ```

- **`walker`** -  A special type of architype that **traverses** a graph, moving between `node` instances along `edge` connections. Walkers define behaviors for navigating structured data.

    ```jac
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:10:10"
    ```


### Create an Architype

Let's start by creating a simple architype named Person. Architypes define entities in Jac and can later be extended with attributes and abilities.

The following example, `obj MyObject` contains ability. So, we'll explore it in **Arributes in Architypes** section.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:21:23"
    ```


### Create Object

Now we can use the obj named MyClass to create the object.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:25:28"
    ```

??? tip "Output"
    ```
    2
    ```

---

## Attributes in Architypes

Architypes can have attributes that store data. Attributes are defined using the `has` keyword.

### Assigning Default Value to Attributes

We can define an attributes,

- without a default value.

**Code Example**
```jac linenums="5"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:37:39"
```

- with a default value.

**Code Example**
```jac linenums="9"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:41:43"
```

!!! note
    You don't need to manually implement an `__init__` function like in Python. Jac automatically handles the initialization of `has` attributes during object creation.


We can define attributes inside any type of Architype.

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:33:51"
```

### Ways of Defining Attributes

- Each attribute on a new line with a separate `has` keyword

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:55:58"
```

- In a single line `has`, seperated by commas `(,)`

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:60:62"
```

### Static Attributes

Static attributes belong to the **architype itself** rather than individual instances. These are defined using the `static has` keyword.

**Code Example**
```jac linenums="6"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:65:71"
```

* Here, `wheels` is a **static attribute**, meaning all `Car` objects share the same value (`4` wheels).


---

## Abilities Inside Architypes

Abilities can be defined inside **architypes** (nodes, edges, objects, etc.).

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:75:97"
    ```

### Static Abilities

Static abilities do not depend on instance data. They are defined using the `static` keyword.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_ability.jac:13:17"
    ```

* This `square` ability does not require an instance of `MathUtils` and can be called directly.


### Overriding Abilities in Inheritance

If an `architype` inherits another, it can override its abilities.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:101:111"
    ```

* Here, `Dog` inherits `Animal` but overrides the `speak` ability with its own behavior.


### Abstract Abilities in Jac

In Jac, abilities define actions or behaviors within an architype. Some abilities can be **abstract**, meaning they provide a blueprint but do not contain actual implementations.

* It must be implemented in child architypes.
* It acts like an interface or contract for derived architypes.
* Declared using the `abs` keyword at the end of the definition.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:114:122"
    ```

!!! warning
    Since `Shape` obj has an abstract ability, an instance cannot be initiated from `Shape`.

    So, This is not valid.
    ```
    with entry {
        s = Shape();
    }
    ```

---

## Inheritance of Architypes

Architypes can **inherit** properties and abilities from other architypes.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:127:134"
    ```

So, now the properties of `Animal` can be accessed through `Pet`.

**Code Example**
    ```jac linenums="9"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:136:140"
    ```


## String Identifiers in Architypes

Architypes can have an optional **string identifier** that describes them.

**Code Example**
    ```jac linenums="1"
    --8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:14:17"
    ```

---

## Implementations for Architypes and Abilities

Jac provides implementations (impls) to extend or define abilities and attributes separately from the original architype definition. This makes the code modular, organized, and easier to maintain.

### Impls for Architypes

Architypes store data and define structures, like objects in OOP. Instead of defining everything inside them, implementations allow modifications later.

**Code Example**
Declaration of the Architype

```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:146:146"
```

Implementation of the Architype
```jac linenums="2"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:148:152"
```

### Impls for Abilities Inside Architypes

In Jac, abilities (`can`) inside architypes (like `walker`, `object`, `node`, etc.) can be **declared separately** from their implementations. This keeps the structure modular and improves clarity.

**Code Example**

Abilities can be **declared inside an architype** without defining their behavior.

```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:155:157"
```

We can implement the ability **outside** the architype declaration.

```jac linenums="5"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architypes.jac:159:161"
```