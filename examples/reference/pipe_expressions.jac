#pipe.jac

with entry {
"hello" |> print;
"hello"|> len |> print;
}

with entry{
    a=5;
    b=3;
    c=2;
    result1 = a|b ?: a|c  ;   #elvish_check
    result2 = b|c ?: c|a ;
    print(result1);
    print(result2);

    print <| result1; 
    print <| type <| "Hello";   # pipe_back
    }
