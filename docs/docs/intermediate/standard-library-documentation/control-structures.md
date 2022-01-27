---
sidebar_position: 4
---

# Control Structures

> Statements which allow you to control the execution flow of the program depending on a condition. 
> Currently the JAC language supports:
> - IF - ELSE - ELIF
> - Switch Case (not yet supported)

## IF-ELSE
```
// prototype

if(condition) {
    code to execute
}else{
    else code to execute
}

// examples

if(a == b): std.out("A equals B");
else: std.out("A is not equal to B");

// or in code block form

if(a == b){
    std.out("A equals B");  
}else{
    std.out("A is not equal to B");
}
```

## IF-ELIF-ELSE

```
if(a == b): std.out("A equals B");
elif(a > b): std.out("A is greater than B");
elif(a == b - 1): std.out("A is one less than B");
elif(a == b - 2): std.out("A is two less than B");
else: std.out("A is something else");
```

## Iterations

> The JAC language supports two types of iterative control structures.
> - While Loop
> - For Loop

### While Loop

```
// prototype
while(condition) {
    code to execute
}

// example
i = 5;
while(i>0) {
    std.out("Hello", i, "times!");
    i -= 1; //update statement
}
```

### For Loop

```
// prototype 
for (initialization statement) to (test_expression) by (update_statement){
    code to execute
}

// example
for i=0 to i<10 by i+=1:
    std.out("Hello", i, "times!");
}
```

> For any given type of loop used you have the ability to exit out of the loop by using the the **break** statement


### Break

```
// for loop example

for i=0 to i<10 by i+=1 {
    std.out("Hello", i, "times!");
    if(i == 6): break;
}

// while loop example

i = 10;
while(i>0) {
    std.out("Hello", i, "times!");
    i -= 1; //update statement
    if(i == 6): break;
}
```

> For any given type of loop used you have the ability to skip the current iteration and contine one to the next by using the the continue statement

### Continue

```
// for loop example

for i=0 to i<10 by i+=1 {
    std.out("Hello", i, "times!");
    if(i == 6): continue;
}

// while loop example

i = 5;
while(i>0) {
    if(i == 3){
        i -= 1; continue;
    }
    std.out("Hello", i, "times!");
    i -= 1;
}
```