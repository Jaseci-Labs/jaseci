node A {
    has val: int;
}

edge E {
    has val: int;
}
with entry {
    (a, b) = (A(5), A(10));
    root +>:E(20):+> a;
    root +:E(25):+> b; # Remove after dropping deprecated syntax support
    b <+:E(30):<+ A(15);
    a <+:E(35):+ A(20); # Remove after dropping deprecated syntax support
    print([root->:E:->]);
    print([a<-:E:<-]);
    print([root-:E:->]); # Remove after dropping deprecated syntax support
    print([a<-:E:-]); # Remove after dropping deprecated syntax support
}
