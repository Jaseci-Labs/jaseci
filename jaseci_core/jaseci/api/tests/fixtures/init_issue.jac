
node simple {has id=1;}

walker init {
    root {
        take --> node::simple else {
            spawn here --> node::simple;
            take --> node::simple;
        }
    }
    simple {
        report here.context;
        disengage;
    }
}