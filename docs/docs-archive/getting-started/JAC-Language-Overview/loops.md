---
title: Loops
---
Loops are written similiar to python it run a specific amount of time as in the case of the "For" loop or until a condition is meet as in the case for the "While" loop.

```jac
walker init {
    # the for loop
    for i=0 to i<10 by i+=1:
        std.out(i)

    #the while loop
    while(x<10){
        std.out(x);
        x = x +1;
    }
}
```
