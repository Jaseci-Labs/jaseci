global node_count=0;
node simple: has id;

walker init {
    has output = [];
    with entry {
        t = here;
        for i=0 to i<10 by i+=1 {
            t = spawn t --> node::simple(id=global.node_count);
            global.node_count+=1;
        }
    }
    take -->;
    simple {
        if(here.id % 2==0): skip;
        if(here.id == 7): disengage;
        output.l::append(here.id);
    }
    output.l::append(here.info['name']);
    with exit: std.out(output);
}