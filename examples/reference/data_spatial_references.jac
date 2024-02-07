node node_a {
    has value: int;
}

walker Creator {
    can create with `<root> entry;
}

edge MyEdge {
    has val: int = 5;
}

:walker:Creator:can:create {
    end = <here>;
    for i=0 to i<4 by i+=1  {
        if i % 2 == 0 {
            end ++> (end := node_a(value=i));
        } else {
            #end +:MyEdge:val=i:+> (end := node_a(value=i + 10));
            #end <+:MyEdge:val=i :+ (end := node_a(value=i + 10));
            print(end);
            <r> <+: MyEdge:val=i :+ end;

        }
    }
}

with entry {
    <root> spawn Creator();

    print(<r>._jac_.gen_dot());
}


