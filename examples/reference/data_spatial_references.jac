node node_a{
    has val:int;
}
walker Creator{
    can create with `<root> entry;
}

edge connector{
    has value:int = 10;
}

:walker:Creator:can:create {
    end = <here>;
    for i=0 to i<3 by i+=1  {
        end ++> (end := node_a(val=i));
    }
    end +:connector:value=i:+> (end := node_a(val=i + 10));
    <root> <+:connector:value=i :+ (end := node_a(val=i + 10));
}

with entry{
    <root> spawn Creator();
    print(<r>._jac_.gen_dot());
}




