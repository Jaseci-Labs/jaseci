---
sidebar_position: 4
---

# Test Drive

Let's test out the JAC language by running a simple programs which utilizes control structures and output statments.

```
walker init {
    x = 34 -30; 
    y = "Hello";
    z = 3.45;

```

Think of the walker as a little robot friend who traverses the nodes and edges of graphs. We initialize the variable of x,y,z. 

```
walker init {
    x = 34 -30; 
    y = "Hello";
    z = 3.45;


if(z==3.45 or y=="Bye"){
    x =x+1;
    y=y+" World" ;

}
```

The IF  statment is very similiar to those of python. Note that after every line there is a semicolon .

```
walker init {
    x = 34 -30; 
    y = "Hello";
    z = 3.45;


if(z==3.45 or y=="Bye"){
    x =x+1;
    y=y+" World" ;
}

std.out(x);
```
std.out() prints any variable passed in to the function on to the terminal.

```
walker init {
    x = 34 -30; 
    y = "Hello";
    z = 3.45;


if(z==3.45 or y=="Bye"){
    x =x+1;
    y=y+" World" ;
}
    
std.out(x);
for i=0 to i<3 by i+=1:
    std.out(x-1,'-',y);

report [x,y+'s'];
}
```

This FOR loop will run 3 times. Printing the values of (x -1) and the value of y. The report list adds data to the payload.

Let's run the program by  oprning the terminal and running:
```
 jsctl jac run class2.jac

 ```

 Your Output should look like this:

 ![alt Output for code](/img/test-drive-output.png)