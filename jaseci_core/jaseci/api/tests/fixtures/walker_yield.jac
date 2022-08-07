walker test_yield {
    has a=6;
    with entry {
        report "entering";
    }

    if(a < 10) {
        a+=1;
        report a;
        yield;
    }
    else {
        report "should start over now";
    }
    with exit {
        report "exiting";
    }
}

walker test_yield_report {
    has a=6;

    if(a < 10) {
        a+=1;
        yield report a;
    }
    else {
        report "should start over now";
    }
}

walker test_yield_disengage {
    has a=6;

    if(a < 10) {
        a+=1;
        yield disengage report a;
        report "test"; #should not be printed
    }
    else: report "should start over now";
}

walker test_yield_take {
    has a=6;

    if(a < 10) {
        a+=1;
        report a;
        yield take here;
        report "test"; #should be printed
    }
    else: report "should start over now";
}

global node_count=0;

node simple {has id;}

walker smart_yield {
    with entry {
        t=here;
        for i=0 to i<10 by i+=1 {
            t = spawn t --> node::simple(id=global.node_count);
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
            t = spawn t --> node::simple(id=global.node_count);
            global.node_count+=1;
        }
    }
    report here.context;
    take -->;
    yield disengage; #hops of graph so must prime for specified continue node
}

walker deep_yield {
    has steps=0;
    with entry {
        for i=0 to i<15 by i+=1 {
            spawn here walker::smart_yield;
        }
    }
    take -->;
    steps+=1;
    with exit {report steps;}
}