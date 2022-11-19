node simple {has a=4,b=5,c=3;}

walker init {
    root {
        new_node = spawn here ++> node::simple;
        report new_node;
    }
}
