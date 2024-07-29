# Separating code Implementation from Declaration

Jac-lang offers a unique feature which allows the coder to separate the functional declaration of the code and their declaration. This facilitate cleaner code without importing required files manually.

## Function Declaration and Function Body

Usually when coding with python the body of a function or a method will be coded right after the function/method declaration (def statement) as shown in the following python code snippet.

```python
from enum import Enum

def foo() -> None:
    return "Hello"

class vehicle:
    def __init__(self) -> None:
        self.name = "Car"

class Size(Enum):
    Small = 1
    Medium = 2
    Large = 3

car = vehicle()
print(foo())
print(car.name)
print(Size.Medium.value)
```
However, Jac-lang offers novel language features which allows a programmer to organize their code effortlessly.

## Separating function/object bodies from their declaration.

In jaclang the declaration of functions and objects can be done independently, as shown in the below code snippet. By doing so, it creates an empty shell for the function/object/enum. 

```python
can foo();

obj vehicle;

enum Size;

test check_vehicle;

with entry {
    car = vehicle();
    print(foo());
    print(car.name);
    print(Size.Medium.value);
}
```
The bodies should be defined somewhere in the codebase for the program to be compiled successfully. The notation for defining the function/object/enum bodies are as follows, for the given example.

```python
:can:foo() {
    return ("Hello");
}

:obj:vehicle  {
    has name: str = "Car";
}

:enum:Size {
    Small=1,
    Medium=2,
    Large=3
}

:test:check_vehicle {
    check assertEqual(vehicle(name='Van').name, 'Van');
}
```

However, there are multiple locations where this code can be held in order for this implementation separation to work.

### Same ```.jac``` file as declaration

The bodies of the objects can be held in the same file as the declaration. This will only improve the code visually during declaration while code management is not sgnificantly improved.

### Including files in ```<>.impl.jac``` / ```<>.test.jac``` files 

If the programmer requires better codebase management with having the implementations together in a separate file, jac-lang facilitates that as well. In the previous example there are implementation of objects/enums/functions as well as test. These can be separated in a separate files living in the base path as the main module, named as ```<main_module_name>.impl.jac``` and ```<main_module_name>.test.jac```. Including or importing these files are not required. The file structure can be shown as follows.

```
base
├── main.jac
├── main.impl.jac
└── main.test.jac
```

However, all implementation files should be located in the base path which can become because of this if there are multiple files, each having their own implementation file.

### Including files in ```<>.impl``` / ```<>.test``` folders

The implementation of the program can be coded within individual .impl and .test folders as well. These folders should be named as ```<main_module_name>.impl``` and ```<main_module_name>.impl```. 

Additional benefits of this separation is that inside the folder the implementations can be broken down into multiple files as per the programmer's preference, as long as each file has the ```.impl.jac``` or ```.test.jac``` suffixes. The file structure can look as follows.

```
base
├── main.jac
│
├── main.impl
│   ├── foo.impl.jac
│   ├── vehicle.impl.jac
│   └── size.impl.jac
│
└── main.test
    └── check_vehicle.test.jac
```

These file separation features in jac-lang allows the programmer to organize their code seamlessly without any extra ```include``` or ```import``` statements.

> **NOTE :**
> Even if adding the suffixes, as described above, to separated files and folders are not done the separated code bodies can still live in separate files and folders as long as they are included in the main module.