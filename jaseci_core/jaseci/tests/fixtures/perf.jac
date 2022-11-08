node a {
    has b, c, d, e, f;
}

type t {
    has a = {
                    "name": "new_snt",
                    "auto_create_graph": "blah blash",
                    "auto_run": false,
                    "set_active": true
    };
    has b = {
                    "name": "new_snt",
                    "auto_create_graph": "blah blash",
                    "auto_run": false,
                    "set_active": true
    };
    has c = {
                    "name": "new_snt",
                    "auto_create_graph": "blah blash",
                    "auto_run": false,
                    "set_active": true
    };
    has d ={
                    "name": "new_snt",
                    "auto_create_graph": "blah blash",
                    "auto_run": false,
                    "set_active": true
    };
}

walker slow {
    has steps=0;
    has biglist=[];
    with entry {
        g=here;
        for i=0 to i<300 by i+=1 {
            g=spawn g --> node::a(b=spawn t::t, c=spawn t::t,
                                  d=spawn t::t, e=spawn t::t, f=spawn t::t);
        }
        take-->;
        internal.start_perf_test();
    }
    a {
        biglist.l::append((*(&here)).context);
        take -->;
        steps+=1;
    }
    with exit {
        std.out(internal.stop_perf_test());
    }
}