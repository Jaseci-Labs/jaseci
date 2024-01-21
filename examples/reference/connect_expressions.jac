import:py random;

walker walker_1 {
    can create with `<root> entry;
}

edge MyEdge {
  has val:int =5;
}

node node_a{
    has val:int;
    can print_some with walker_1 entry;
}
node node_b{
    has value:int;
}

:walker:walker_1:can:create{
    end = <here>;   
    for i = 0 to i<5 by i+=1{
        end ++> end := node_a(val=i+1);
    }
    #connect 3 nodes of node_b from the last node_a created
    for i=0 to i<3 by i+=1 {
        node_a(val=3) +:MyEdge:val=random.randint(1,10):+> node_b(value=i+5);
    }
    visit-->;
}

:node:node_a:can:print_some{
    print(f"this is {<self>}");
    
    visit-->;
}

with entry{
    <root> spawn walker_1();
    <root>._jac_.gen_dot();
}