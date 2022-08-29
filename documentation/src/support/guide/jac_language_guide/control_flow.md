# Control Flow



## Select Statement 

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



## For and While loop



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

