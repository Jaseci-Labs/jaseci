node simple: has id, anchor anc=5.4, private priv="Test";
global count=0;

walker pack_it {
    has to_pack=[];
    with entry {
        t=here;
        to_pack.l::append(here);
        for i=0 to i<5 by i+=1 {
            to_pack.l::append(
                spawn t --> node::simple(id=global.count)
            );
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
    }
    report net.pack(to_pack);
}

walker pack_it_subgraph {
    has to_pack=[];
    with entry {
        t=here;
        for i=0 to i<5 by i+=1 {
            spawn t --> node::simple(id=global.count);
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
    }
    report net.pack(to_pack);
}

walker pack_unpack {
    has to_pack=[];
    has count=0;
    with entry {
        t=here;
        for i=0 to i<5 by i+=1 {
            spawn t --> node::simple(id=global.count);
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
        val = net.pack(to_pack);
        new = net.unpack(val);
        here --> new[0];
    }
    take -->;
    count+=1;
    with exit {
        report count;
    }
}

walker pack_unpack_terse {
    has to_pack=[];
    has count=0;
    with entry {
        t=here;
        for i=0 to i<5 by i+=1 {
            spawn t --> node::simple(id=global.count);
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
        here --> net.unpack(net.pack(to_pack))[0];
    }
    take -->;
    count+=1;
    with exit {
        report count;
    }
}

walker pack_it_destroy {
    has to_pack=[];
    with entry {
        t=here;
        to_pack.l::append(here);
        for i=0 to i<5 by i+=1 {
            to_pack.l::append(
                spawn t --> node::simple(id=global.count)
            );
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
        net.pack(to_pack, true);
    }
    take -->;
    report here;
}

walker pack_it_anc_priv {
    has to_pack=[], p;
    with entry {
        t=here;
        for i=0 to i<5 by i+=1 {
            t=spawn t --> node::simple(id=global.count);
            to_pack.l::append(t);
            global.count+=1;
        }
        p = net.pack(to_pack, true);
    }
    root {
        up=net.unpack(p);
        here --> up[0];
    }
    take --> node::simple == 5.4;
    report here;
}