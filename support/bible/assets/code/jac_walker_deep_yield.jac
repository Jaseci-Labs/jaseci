global node_count=0;

node simple {has id;}

walker simple_yield {
    with entry {
        t=here;
        for i=0 to i<10 by i+=1 {
            t = spawn t --> node::simple(id=global.node_count);
            global.node_count+=1;
        }
    }
    yield take -->;

}

walker deep_yield {
    for i=0 to i<16 by i+=1 {
        spawn here walker::simple_yield;
    }
}