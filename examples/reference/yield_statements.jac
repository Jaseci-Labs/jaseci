#example 1
can foo(){
    for i in range(3){
        yield i;
        }
}

with entry{
    for i in foo(){
        print("Yielded:", i);
        }
}

#Example 2
can fibonacci(n:int){
    (a, b ) = (0, 1) ;
    count = 0 ;

    while count < n{
        yield a ;
        (a, b) = (b, a + b) ;
        count += 1 ;
    }
}
with entry{
    number = int(input("Enter a Number: "));
    for num in fibonacci(number){
        print(num);
    }
}