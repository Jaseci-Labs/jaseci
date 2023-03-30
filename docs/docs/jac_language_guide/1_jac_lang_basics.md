# Jaseci Language Basics

Welcome to the exploration of the basic features of Jaseci. As a versatile programming language, Jaseci offers a wide range of capabilities that are found in other programming languages. In this section, we will delve into the core features of Jaseci, including input and output, a variety of data types, arithmetic and logical operators, comparison operators, and assignment operators. So, let's get started and uncover the full potential of Jaseci!

- [Jaseci Language Basics](#jaseci-language-basics)
  - [Data Types](#data-types)
    - [Special Types](#special-types)
    - [Typecasting](#typecasting)
  - [Operators](#operators)
    - [Arithmatic Operators](#arithmatic-operators)
    - [Equality Operations](#equality-operations)
    - [Logical Operators](#logical-operators)
    - [Assigments Operators](#assigments-operators)
- [Precedence of Jaseci Operators](#precedence-of-jaseci-operators)

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
### Assigments Operators

```jac
a = 4 + 4;
a += 4 + 4;
a -= 4 * -5;
a *= 4 / 4;
a /= 4 - 6;
```

# Precedence of Jaseci Operators

| Rank | Symbol                           | Description                                    |
| ---- | -------------------------------- | ---------------------------------------------- |
| 1    | ( ), [ ], ., ::, spawn           | Parenthetical/grouping, node/edge manipulation |
| 2    | ^, []                            | Exponent, Index                                |
| 3    | *, /, %                          | Multiplication, division, modulos              |
| 4    | +, -                             | Addition, subtraction                          |
| 5    | ==, !=, >=, <=, >, <, in, not in | Comparison                                     |
| 6    | &&,                              |                                                | , and, or | Logical |
| 7    | ++>, <++, +[]+>, <+[]+           | Connect                                        |
| 8    | =, +=, -=, *=, /=, :=            | Assignment                                     |
