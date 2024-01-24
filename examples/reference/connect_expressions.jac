import:py random;

walker walker_1 {
    can create with `<root> entry;
}

node node_a{
    has val:int;
    can print_some with walker_1 entry;
}

walker walker_2{
    can travel with `<root>|node_a entry;
}
node node_b{
    has value:int;
    can do with walker_2 entry;
    can print_one with walker_1 entry;
}

edge MyEdge {
  has val:int =5;
}

:walker:walker_1:can:create{
    end = <here>;
    for i = 0 to i<5 by i+=1{
        end ++> end := node_a(val=i+1);
        #connect three nodes of node_b from node_a(val=3)
        if i == 2{
            for j=0 to j<3 by j+=1 {
                end +:MyEdge:val=random.randint(1,5):+> node_b(value=j+10);
            }

        }
    }
    #connect 3 nodes of node_b from the last node_a created
    for i=0 to i<3 by i+=1 {
        end +:MyEdge:val=random.randint(1,5):+> node_b(value=i+5);
    }
    visit-->;
}
:walker:walker_2:can:travel{
    print("Hi, this is walker_2");
    for i in -:MyEdge:val<=5 :->{
            print(i.val);
        }
    visit-->;
}


:node:node_a:can:print_some{
    print(f"this is {<self>}");
    visit--> ;
}
:node:node_b:can:do{
    print("Hey there!");
    visit-->;
    }
:node:node_b:can:print_one{
    print(f"This is {<self>}, Welcome walker_1!! ");
}

with entry{
    <root> spawn walker_1();
    <root> spawn walker_2();
    #<root>._jac_.gen_dot();
}