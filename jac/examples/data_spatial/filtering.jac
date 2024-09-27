node A{
    has val:int =0;
}
node B{
    has val:int =0;
}
node C{
    has val:int =0;
}

edge a{}

edge b{}

edge c{}

with entry{
    Start = A(5);
    root +:a:+> Start;
    Start +:b:+> B(10) +:c:+> C(15);
    Start +:b:+> A(20) +:a:+> C(25);

    print([root-->-:b:->(`?A)]);
    print([root-:a:-> -:b:-> -:c:->(`?C)]);
    print([root-:a:-> -:b:-> -:c:->(`?C)]);
}