---
sidebar_position: 1
---

# Jaseci Language Basics

Welcome to the exploration of the basic features of Jaseci. As a versatile programming language, Jaseci offers a wide range of capabilities that are found in other programming languages. In this section, we will delve into the core features of Jaseci, including input and output, a variety of data types, arithmetic and logical operators, comparison operators, and assignment operators. So, let's get started and uncover the full potential of Jaseci!

## Data Types

JAC is a dynamically typed language so there is no need to declare the data type.

```jac
walker init {
    a=5;
    b=5.0;
    c=true;
    d='5';
    e=[a, b, c, d, 5];
    f={'num': 5};

    summary = {'int': a, 'float': b, 'bool': c, 'string': d, 'list': e, 'dict': f};

    std.out(summary);
}
```

```jac
walker init {
    a=5;
    std.out(a.type, '-', a);
    a=5.0;
    std.out(a.type, '-', a);
    a=true;
    std.out(a.type, '-', a);
    a=[5];
    std.out(a.type, '-', a);
    a='5';
    std.out(a.type, '-', a);
    a={'num': 5};
    std.out(a.type, '-', a);
 }
```
**Output**
```
JAC_TYPE.INT - 5
JAC_TYPE.FLOAT - 5.0
JAC_TYPE.BOOL - true
JAC_TYPE.LIST - [5]
JAC_TYPE.STR - 5
JAC_TYPE.DICT - {"num": 5}
```
### Special Types
```jac
walker init {
    a=null;
    std.out(a.type, '-', a);
    a=str;
    std.out(a.type, '-', a);
    std.out(null.type);
    std.out(null.type.type);
 }
```
**Output**
```
JAC_TYPE.NULL - null
JAC_TYPE.TYPE - JAC_TYPE.STR
JAC_TYPE.NULL
JAC_TYPE.TYPE
```
### Typecasting
```jac
walker init {
    a=5.6;
    std.out(a+2);
    std.out((a+2).int);
    std.out((a+2).str);
    std.out((a+2).bool);
    std.out((a+2).int.float);
    if(a.str.type == str and !(a.int.type == str) and a.int.type == int):
        std.out("Types comes back correct");

    # can cast a dictionary to json string
    val={"test": 1}.str;
    std.out(val, val.type);

    # can cast json string to dictionary
    val='{"test2": 2}'.dict;
    std.out(val, val.type);
}
```
**Output**
```
7.6
7
7.6
true
7.0
Types comes back correct
{"test": 1} JAC_TYPE.STR
{"test2": 2} JAC_TYPE.DICT
```

## Operators

### Arithmatic Operators

```jac
// addition
a = 4 + 4;
e = a + b + c + d;

// multiplication
b = 4 * -5;

// division
c = 4 / 4;  # Returns a floating point number

// subtraction
d = 4 - 6;

// exponent / power
a = 4 ^ 4;

// modulus
b = 9 % 5

```
### Equality Operations
```jac
// equal
a == b

// not equal
a != b

// less than
a < b

// greater than
a > b

// less than and equal to
a <= b

// greater than and equal to
a >= b
```

### Logical Operators
```jac
// not
!a,

// and
a && b
a and b

// or
a || b
a or b

// mixture
!a or b
!(a and b)
```
### Assignment Operators

```jac
a = 4 + 4;
a += 4 + 4;
a -= 4 * -5;
a *= 4 / 4;
a /= 4 - 6;
```

## Precedence of Jaseci Operators

| Rank | Symbol                           | Description                                    |
| ---- | -------------------------------- | ---------------------------------------------- |
| 1    | ( ), [ ], ., ::, spawn           | Parenthetical/grouping, node/edge manipulation |
| 2    | ^, []                            | Exponent, Index                                |
| 3    | *, /, %                          | Multiplication, division, modulo               |
| 4    | +, -                             | Addition, subtraction                          |
| 5    | ==, !=, >=, <=, >, <, in, not in | Comparison                                     |
| 6    | &&,                              |                                                | , and, or | Logical |
| 7    | ++>, <++, +[]+>, <+[]+           | Connect                                        |
| 8    | =, +=, -=, *=, /=, :=            | Assignment                                     |

## Input and Output in Jaseci

To print on to the terminal we use :

```jac
std.out("Hello World");
```

To take input from  terminal we use :
```jac
std.input();

```
## File Handling in Jaseci

Load contents of a file to string.

```jac
lines  = file.load_str("test.txt")
```

Load the contents of a Json file.
```jac
lines = file.load_json("tests.json");
```

## Global Variables in Jaseci

Global variables are variables that can be accessed anywhere in your application. They can be useful for storing values that are used frequently or that need to be accessed from different parts of your code.

### Declaring a Global Variable

To declare a global variable in Jac, you can use the global keyword followed by the name of the variable and its initial value. For example:

```jac
//global variable_name = value
global transportation = "Airplane";
```

This tells the interpreter that the variable is a global variable and can be accessed from anywhere in your code.


### Accessing a Global Variable

To access a global variable in Jac, you use the syntax global.variable_name. For example:

Example Code:

```jac
//global.variable_name
walker init{
    transport_mode = global.transportation;
    std.out(transport_mode);
}
```

Expected Output:

```
Airplane
```

This syntax tells the interpreter to look for the variable in the global scope, rather than the local scope.

It's important to note that overusing global variables can make your code harder to understand and maintain, so use them judiciously. In general, it's a good practice to limit the scope of your variables to the smallest scope possible.

### Global Reference Syntax (to be improve)

This for accessing current thread attributes.

#### Context

`global.context`

It will return global variables.

#### Info

`global.info`

 - report
 - report_status
 - report_custom
 - request_context
 - runtime_errors

`global.info["report"]`

Returns current report list

```json
[1, "any value from report", {}, true, []]
```

`global.info["report_status"]`

Returns http status code for the report

```json
    200
```

`global.info["report_custom"]`

Returns current report:custom value

```json
{
  "yourCustomField": "customValue"
}
```

`global.info["request_context"]`

Returns current request payload
```json
{
  "method": "POST",
    "headers": {
        "Content-Length": "109",
        "Content-Type": "application/json",
        "Host": "localhost:8000",
        "User-Agent": "insomnia/2022.4.2",
        "Accept": "*/*"
         },
    "query": {},
      "body": {
        "name": "sample_walker",
        "ctx": {
             "fieldOne": "1"
            },
            "nd": "active:graph",
           "snt": "active:sentinel"
        }
}
```

#### Usage:

Walker can now accept custom payload (non ctx structure). Request body can be access via `globa.info["request_context"]["body"]`
Developers now have control on different request constraints such us method type and headers validation

`global.info["runtime_errors"]`

Returns current runtime error list.

```json
[
"sentinel1:sample_walker - line 100, col 0 - rule walker - Internal Exception: 'NoneType' object has no attribute 'activity_ability_ids'"
]
```

## Working with Imports

One of the most important aspects of any coding language is the ability to efficiently organize code and build programs. In Jaseci, we use imports to make this process as simple and intuitive as possible.

### Importing Files

In Jaseci, you can easily import entire files using the following syntax:

```jac
import {*} with "path_to_file"
```

For example, to import an entire file called conv_walkers.jac, you would use:

```jac
import {*} with "./conv_walkers.jac"
```

This will import all of the graphs, nodes, and walkers contained in the specified file.

### Importing Specific Parts of a File

If you only need to import specific parts of a file, you can use the following syntax:

```jac
// import {feature::name, feature::{name, name}} with "path_to_file"
// you can replace features with abstractions like nodes, edges, graphs and walkers
// replace name with the name of the abstraction in your file
import {graph::dummy, node::{banana, apple}} with "path_to_file"
```
In this example, we are importing the dummy graph, as well as the banana, and apple nodes from the file located at `path_to_file`.

You can specify which types of objects you want to import (graphs, nodes, or walkers) by replacing graph in the above example with either node or walker.

Example:

```jac
 import {graph::dummy, node::{banana, apple, testnode}} with "./jac_tests.jac";
 import {*} with "./jac_tests.jac";
 import {graph::dummy, node*} with "./jac_tests.jac";

 walker init {
    has num=4;
    with entry {
        spawn here ++> graph::dummy;
    }
    report here.context;
    report num;
    take -->;
}
```

Output:

```
{
    "success": true,
    "report": [
        {},
        4,
        {
            "yo": "Hey yo!",
            "bro": null
        },
        4,
        {
            "x1": "I'm banana",
            "x2": null
        },
        4
    ]
}
```