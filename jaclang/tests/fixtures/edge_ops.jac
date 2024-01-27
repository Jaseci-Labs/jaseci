import:py random;

walker Creator {
    can create with `<root> entry;
}

node node_a{
    has val:int;
}

walker Travelor{
    can travel with `<root>|node_a entry;
}
node node_b{
    has value:int;
}

edge MyEdge {
  has val:int =5,
      val2:int = 10;
}

:walker:Creator:can:create{
    end = <here>;
    for i = 0 to i<5 by i+=1{
        end ++> end := node_a(val=i+1);
        #connect three nodes of node_b from node_a(val=3)
        if i == 2{
            for j=0 to j<3 by j+=1 {
                end +:MyEdge:val=random.randint(1,15), val2=random.randint(1,5):+> node_b(value=j+10);
            }
            print([(i.val, i.val2) for i in list(end._jac_.edges.values())[1]]);
        }
    }

    #connect 3 nodes of node_b from the last node_a created
    for i=0 to i<3 by i+=1 {
        end +:MyEdge:val=random.randint(1,20):+> node_b(value=i+5);
    }

    visit-->;
}
:walker:Travelor:can:travel{
    for i in -:MyEdge:val<=5:-> {
            print(i.value);
        }
    visit-->;
}

with entry{
    random.seed(1);
    <root> spawn Creator();
    <root> spawn Travelor();
    #<root>._jac_.gen_dot();
}