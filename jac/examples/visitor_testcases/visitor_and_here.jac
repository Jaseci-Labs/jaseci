node A{
    has val:int =0;
}

node B{
    has val:int =0;
}

edge a{
}

edge b{
}

walker W1{
    can create with `root entry;
}

walker W2{
    can create with `root entry;
}

:walker:W1:can:create{
    One = A(5);
    Two = A(30);
    visitor +>:a:+> Two;
    One +>:a:+> A(10) +>:a:+> A(15);
    One +>:a:+> A(20) +>:a:+> A(25);
    Two +>:a:+> A(40) +>:a:+> A(50);
    visitor +>:a:+> One;

}

:walker:W2:can:create{
    One = B(5);
    Two = B(30);
    here +>:a:+> Two;
    One +>:b:+> B(10) +>:b:+> B(15);
    One +>:b:+> B(20) +>:b:+> B(25);
    Two +>:b:+> B(40) +>:b:+> B(50);
    here +>:b:+> One;

}
    
with entry{
    root spawn W1();
    print([root-->-->(`?A)]);
    print([root--> --> -->(`?A)]);

    root spawn W2();
    print([root-->-->(`?B)]);
    print([root--> --> -->(`?B)]);

}