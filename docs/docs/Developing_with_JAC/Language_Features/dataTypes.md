---
title : Data Types
---


## Data types
JAseci is a dynamically typed language so there is no need to specify the data type.
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