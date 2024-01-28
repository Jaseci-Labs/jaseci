import:py random;

node node_a{
    has value:int;
}

walker Creator {
    can create with `<root> entry;
    can travel with `<root>|node_a entry;
}

edge MyEdge {
  has val:int =5;
}

:walker:Creator:can:create{
    end = <here>;
    for i = 0 to i<8 by i+=1{
        if i % 2 == 0{
            end ++> end := node_a(value=i+1);
        }
        else{
            end +:MyEdge:val=random.randint(1,8):+> node_a(value=i+10);
        }
    }
}
:walker:Creator:can:travel{
    #print the node values that is connected with MyEdge edges of val less than 5
    for i in -:MyEdge:val<=5 :->{
            print(i.value);
        }
    visit-->;
}

with entry{
    random.seed(3);
    <root> spawn Creator();
    #print(<root>._jac_.gen_dot());
}