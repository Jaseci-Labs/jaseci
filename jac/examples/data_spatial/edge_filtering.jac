node A {
    has val: int = 0;
}


edge a {
    has val: int = 0;
}


edge b {
    has val: int = 0;
}


with entry {
    root +>:a:val=10:+> A(10);
    root +>:a:val=20:+> A(20);
    root +>:b:val=30:+> A(30);
    print([root-->]);
    print([root->:a:->]);
    print([root->:a:val <= 15:->]);
    print([root->:a:val >= 20:->]);
}
