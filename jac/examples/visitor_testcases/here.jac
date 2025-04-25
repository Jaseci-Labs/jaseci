node A{
    has val:int =0;
}

edge a{
}

walker W1{
    can create with `root entry;
}

:walker:W1:can:create{
    One = A(5);
    Two = A(30);
    here +>:a:+> Two;
    One +>:a:+> A(10) +>:a:+> A(15);
    One +>:a:+> A(20) +>:a:+> A(25);
    Two +>:a:+> A(40) +>:a:+> A(50);
    here +>:a:+> One;
}

with entry{
    root spawn W1();
    print([root-->-->(`?A)]);
    print([root--> --> -->(`?A)]);
}