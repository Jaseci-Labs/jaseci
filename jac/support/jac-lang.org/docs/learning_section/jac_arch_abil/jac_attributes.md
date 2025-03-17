### **Attributes in Architypes**
Architypes can have attributes that store data. Attributes are defined using the `has` keyword.

---

### **Assigning Default Value to Attributes**

We can define an attributes,

- without a default value.

**Code Example**
```jac linenums="5"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_attributes.jac:5:7"
```

- with a default value.

**Code Example**
```jac linenums="9"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_attributes.jac:9:11"
```
<br>

We can define attributes inside any type of Architype.

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_arch_attributes.jac"
```

---

### **Ways of Defining Attributes**

- Each attribute on a new line with a separate `has` keyword

**Code Example**
```jac linenums="1"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_attr_inline_has.jac:1:4"
```

- In a single line `has`, seperated by commas `(,)`

**Code Example**
```jac linenums="6"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_attr_inline_has.jac:6:8"
```

---

### **Static Attributes**

Static attributes belong to the **architype itself** rather than individual instances. These are defined using the `static has` keyword.

**Code Example**
```jac linenums="6"
--8<-- "/home/malithaprabhashana/programming/intern/jaseci/jac/examples/learning_section/jac_arch_abil/jac_attr_static.jac"
```

* Here, `wheels` is a **static attribute**, meaning all `Car` objects share the same value (`4` wheels).
