with entry{
    can foo(a: int, b:int)-> int{
       return 8*(a+b);
    }
     
     print(foo(5,4));
     print(foo(9 if 5/2 == 1 else 5,4));
}