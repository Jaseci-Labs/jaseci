---
title : Control Flow
---
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
## Sample Snippets
```jac
walker init {
     a = 4; b = 5;
     if(a == b): std.out("A equals B");
     elif(a > b): std.out("A is greater than B");
     elif(a == b - 1): std.out("A is one less than B");
     elif(a == b - 2): std.out("A is two less than B");
     else: std.out("A is something else");
 }
```
**Output**
```
A is one less than B
```

```jac
walker init {
     for i=0 to i<10 by i+=1:
     std.out("Hello", i, "times!");
 }
```
**Output**
```
Hello 0 times!
Hello 1 times!
Hello 2 times!
Hello 3 times!
Hello 4 times!
Hello 5 times!
Hello 6 times!
Hello 7 times!
Hello 8 times!
Hello 9 times!
```

```jac
walker init {
     my_list = [1, 'jon', 3.5, 4];
     for i in my_list:
     std.out("Hello", i, "times!");
 }
```
**Output**
```
Hello 1 times!
Hello jon times!
Hello 3.5 times!
Hello 4 times!
```

```jac
walker init {
     i = 5;
     while(i>0) {
          std.out("Hello", i, "times!");
          i -= 1;
     }
 }
```
**Output**
```
Hello 5 times!
Hello 4 times!
Hello 3 times!
Hello 2 times!
Hello 1 times!
```

```jac
walker init {
     for i=0 to i<10 by i+=1 {
          std.out("Hello", i, "times!");
          if(i == 6): break;
     }
 }
```
**Output**
```
Hello 0 times!
Hello 1 times!
Hello 2 times!
Hello 3 times!
Hello 4 times!
Hello 5 times!
Hello 6 times!
```

```jac
walker init {
     i = 5;
     while(i>0) {
          if(i == 3){
               i -= 1; continue;
          }
          std.out("Hello", i, "times!");
          i -= 1;
     }
 }
```
**Output**
```
Hello 5 times!
Hello 4 times!
Hello 2 times!
Hello 1 times!
```