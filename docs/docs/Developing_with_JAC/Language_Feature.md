---
sidebar_position: 2
---

# Language Features

## Input and Output 

To print on to the terminal we use :

```jac 
std.out("Hello World");

```

To take input from  terminal we use :
```jac
std.input();

```

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

## Operators

### Arthimetic
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
### Equality
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

### Logical
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
### Assigments
```jac
a = 4 + 4;
a += 4 + 4;
a -= 4 * -5;
a *= 4 / 4;
a /= 4 - 6;
```
## Control FLow 
The If statement

```jac 
# Simple IF statement
if(condition){
    #execute if condition is true
}
```

*If else*
```jac

if(condition){
    #execute code if condition is true
} else {
    # execute code if condition is not true.
}
```
*elif*
```jac 
if(condition){
     #execute code if condition is true
} 
elif(condition 2){
     #execute code if condition 2 is true
}
elif(condition 3){
     #execute code if condition 3 is true
}
else {
     #execute code if none of the conditions are true
}
```
## Functions and Actions

Nodes and Walkers have 