node a {}
node b {}

walker init {
    root {
        spawn here ++> node::a;
        spawn here ++> node::b;
        take -->;
    }

    a, b {
        report here;
    }
}