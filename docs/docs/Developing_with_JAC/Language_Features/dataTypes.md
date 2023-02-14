---
title : Data Types
---


## Data types
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

    std.out(sumary);
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
## Special Types
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
## Typecasting
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
```