node a{}
edge e{}

walker sample {
    can enter with `root entry {
        [-->];
        [-->-->];
        [<--<--];
        [--><--<-->];

        [root->:e:val==2:->];
        [here-->(`?a:val==2)];
        [here->:e:val==2:->-->(`?a:val==2)];

        [edge -->];
        [edge -->-->];
        [edge <--<--];
        [edge --><--<-->];
        bb = [a()];
        [edge root->:e:val==2:->];
        [edge here-->[a()]];
        [edge here->:e:val==2:->-->(`?a:val==2)];
    }
}