global node_count=0;

node simple {has id;}

walker smart_yield {
    with entry {
        t=here;
        for i=0 to i<10 by i+=1 {
            t = spawn t ++> node::simple(id=global.node_count);
            global.node_count+=1;
        }
    }
    report here.context;
    yield;
    take -->;
}

walker smart_yield_no_future {
    with entry {
        t=here;
        for i=0 to i<10 by i+=1 {
            t = spawn t ++> node::simple(id=global.node_count);
            global.node_count+=1;
        }
    }
    report here.context;
    take -->;
    yield disengage; #hops of graph so must prime for specified continue node
}