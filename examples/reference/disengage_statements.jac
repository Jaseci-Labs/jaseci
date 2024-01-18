walker walker_1{
     can func2 with `<root> entry;
}
node node_1{
    has val :int;
     can func_1 with walker_1 entry;
}
:node:node_1:can:func_1{
        print("visiting ",<s>);
        if <s>.val==3{
            print("Disengaging traversal in node with value 3.");
            disengage;
        }
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
node node2{
    has val2:int;
}
with entry{
         <root> spawn walker_1();
}
