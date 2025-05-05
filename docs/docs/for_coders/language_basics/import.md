# Imports

<!-- ## Import Statement
Describe how to import jac module into other jac files
import vs include
Give an example for both.

## Import python module
import:py example. -->

## Import Statement

The ```import``` statement in jac, is used to include code from other Jac modules into the current program, allowing for code reuse and modular organization of the codebase. However, as jac is supersetting python, it allows importing of python modules as well as python libraries.

The functionality of this keyword remains same as in regular python but the syntax has been changed for better readability.

=== "import:jac"
```jac linenums="1"
import:jac module1;
import:jac module2 as mod;
import:jac from module3 { foo as f, bar }
```

The ```:jac``` annotation informs the jac compiler that it should be importing a jac module. The other main difference from regular python syntax is the use of ```from``` keyword which is used before the module unlike in python and all entities imported from the module are placed within curly braces.

=== "import:py"
```jac linenums="1"
import:py os;
import:py datetime as dt;
import:py from math { sqrt as square_root, log }
```

The above deiscription for importing python modules holds as long as the ```:py``` annotation is used.

## Include Statement

Include statement in jac allows the programmer to separate their code into different modules and patch them into a single module.

=== "main.jac"
    ```jac linenums="1"
    include global_vars;

    with entry {
        print('Name:', name);
        print('Age:', age);
    }
    ```
=== "main_import.jac"
    ```jac linenums="1"
    import:jac from global_vars {name, age}

    with entry {
        print('Name:', name);
        print('Age:', age);
    }
    ```
=== "global_vars.jac"
    ```jac linenums="1"
    glob name:str = 'Mason';
    glob age:int = 15;
    ```
In the above example, the global variables are defined in the 'global_vars.jac' module. As the 'main.jac' module includes the 'global_vars.jac' we can use the variables as if they were defined in 'main.jac'. Similar functionality for using ```import:jac``` is shown in the 'main_import.jac' tab, where all required objects must be named in the `import` statement which can be avoided by using `include` instead.