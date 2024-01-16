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
    number = 15;
    for num in fibonacci(number){
        print(num);
    }
}