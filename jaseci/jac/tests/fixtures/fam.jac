node man;
node woman;

edge mom;
edge dad;
edge married;

walker create_fam {
    can init with root entry {
        spawn here ++> node::man;
        spawn here ++> node::woman;
        --> node::man +<-[married]-> --> node::woman;
        take -->;
    }
    can live with woman entry {
        son = spawn here <+[mom]+ node::man;
        son +-[dad]-> <-[married]->;
    }
    can chill with man entry {
        std.out("I didn't do any of the hard work.");
    }
}
