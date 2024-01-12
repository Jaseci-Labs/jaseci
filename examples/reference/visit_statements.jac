walker walker_1{
     can func2 with `<root> entry;
}
node node_1{
    has val :int;
     can func_1 with walker_1 entry;
}
walker walker_2{
    can func_3 with `<root> entry;
}
:node:node_1:can:func_1{
        print("visiting ",<s>);
        visit-->else{
                   print("finished visitng all nodes  ....\n");
                 };
 }
:walker:walker_1:can:func2{
    end = <here>;
    for i=0 to i<5 by i+=1 {
        end ++>  end := node_1(val=i+1);
    }
    visit -->;
}
:walker:walker_2:can:func_3{
        print("visiting specific node by w3\n");
        visit(node_1(val=2));
}
node node2{
    has val2:int;
}
with entry{
         <root> spawn walker_1();
         <r> spawn walker_2();
}
