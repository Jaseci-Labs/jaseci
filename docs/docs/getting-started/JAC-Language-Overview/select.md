---
title: Select Statement
---


```jac
# simple If statement
walker init {
    x = 3.56;
    y = "X is not equal to 3.45";

    if (x ==3.45) {
        std.out(x);
    }
    elif (x==3.56){
        std.out("it's a match");
    }
     else {
        std.out(y);
    }
}

```
Other Conditional statements like < , > ,!= , "and" and "or" are also supported.
