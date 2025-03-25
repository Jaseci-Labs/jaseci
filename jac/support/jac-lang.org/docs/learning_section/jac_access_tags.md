# Access Tags in Jac

In Jac, **Access Tags** control the visibility and accessibility of various elements like,

- architypes
- attributes (`has`)
- abilities (`can`)
- enumerations (`enum`)
- global variables (`glob`)

These tags ensure proper encapsulation and prevent unintended access.


## Types of Access Tags

Jac provides three main access levels:

| Access Tag | Description |
|----------|----------|
| `pub`   | **(Public)** - Accessible from anywhere   |
| `protect`    | **(Protected)** - Accessible within the same scope and derived elements   |
| `priv`    | **(Private)** - Accessible only within the same scope   |


## Access Tags for Global Variables

Global variables in Jac can also be restricted using access tags.