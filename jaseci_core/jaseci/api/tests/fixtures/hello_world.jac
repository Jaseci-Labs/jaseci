node simple: has msg;

walker init {
    has wrld="world";
    report "hello "+wrld+"!";
}

walker one_node {
    with entry {
        spawn here --> node::simple(msg="hello world");
    }
    take --> else {report here;}
}