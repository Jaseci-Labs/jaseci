import:py random;

walker Creator {
    can create with `<root> entry;
}

node node_a{
    has value:int;
}

walker Travelor{
    can travel with `<root>|node_a entry;
}

edge MyEdge {
  has val:int =5;
}

:walker:Creator:can:create{
    end = <here>;
    for i = 0 to i<5 by i+=1{
        end ++> end := node_a(value=i+1);
        #connect three nodes of node_b from node_a(val=3)
        if i == 2{
            for j=0 to j<3 by j+=1 {
                end +:MyEdge:val=random.randint(1,5):+> node_a(value=j+10);
            }
        }
    }
    #connect 3 nodes of node_b from the last node_a created
    for i=0 to i<3 by i+=1 {
        end +:MyEdge:val=random.randint(1,15):+> node_a(value=i+5);
    }
    visit-->;
}
:walker:Travelor:can:travel{
    #print the node values that is connected with MyEdge edges of val less than 5
    for i in -:MyEdge:val<=5 :->{
            print(i.value);
        }
    visit-->;
}

with entry{
    <root> spawn Creator();
    <root> spawn Travelor();
    #<root>._jac_.gen_dot();
}