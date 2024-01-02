with entry{
   
   can foo(x: int, v: int, u: int) -> int{
    return f"The result is: {x|v * u }";
    }

   # Function call with a mix of positional and named parameters
   print(foo(8, v=9 if 5 / 2 == 1 else 5, u=7));

}