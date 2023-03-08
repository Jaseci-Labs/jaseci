import {*} with "extras.jac";

node house {
    has msg;
}

node person;

walker init {
    has a;
    has b;

    root {
        spawn here +[test_edge]+> node::house;
        spawn here walker::extra_walker;
        std.actload_local("hello world");
    }
}

walker count_members {
}
edge sample;
edge test_edge {
    has apple;
}
















