node man;
node woman;

edge mom;
edge dad;
edge married;

walker create_fam {
    root {
        spawn here --> node::man;
        spawn here --> node::woman;
        --> node::man <-[married]-> --> node::woman;
        take -->;
    }
    woman {
        son = spawn here <-[mom]- node::man;
        son -[dad]-> <-[married]->;
    }
    man {
        #std.out("I didn't do any of the hard work.");
    }
}
