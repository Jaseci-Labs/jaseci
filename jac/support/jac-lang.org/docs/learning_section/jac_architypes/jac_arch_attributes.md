Architypes can have attributes that store data. Attributes are defined using the `has` keyword.

## Assigning Default Value to Attributes

We can define an attributes,

- without a default value.

**Code Example**
```jac linenums="5"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:5:7"
```

- with a default value.

**Code Example**
```jac linenums="9"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:9:11"
```

!!! note
    You don't need to manually implement an `__init__` function like in Python. Jac automatically handles the initialization of `has` attributes during object creation.


We can define attributes inside any type of Architype.

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:1:19"
```

---

## Ways of Defining Attributes

- Each attribute on a new line with a separate `has` keyword

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:23:26"
```

- In a single line `has`, seperated by commas `(,)`

**Code Example**
```jac linenums="6"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:28:30"
```

---

## Static Attributes

Static attributes belong to the **architype itself** rather than individual instances. These are defined using the `static has` keyword.

**Code Example**
```jac linenums="6"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_architype/jac_arch_attributes.jac:33:39"
```

* Here, `wheels` is a **static attribute**, meaning all `Car` objects share the same value (`4` wheels).
