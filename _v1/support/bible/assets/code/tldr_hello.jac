walker init {
    x = 34 - 30;  # This is a comment
    y = "Hello";
    z = 3.45;

    if(z==3.45 or y=="Bye"){  # if statement with only thing true
        x=x-1;
        y=y+" World";  # the + between two strings concatinate them
    }

    std.out(x);
    for i=0 to i<3 by i+=1:  # For loop with single line block style
        std.out(x-i,'-', y);  # prints to screen
    report [x, y+'s'];  # adds data to payload
}