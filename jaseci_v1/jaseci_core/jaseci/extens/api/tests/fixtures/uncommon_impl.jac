node with_ability {
    can check with check_ability entry {
        report jaseci.master_self();
        report --> node::inner_node;
    }
}

node inner_node {}

walker init {
    root {
        spawn here ++> node::with_ability;
    }
}

walker check_ability {
    root {
        take --> node::with_ability else {
            n = spawn here ++> node::with_ability;
            spawn n ++> node::inner_node;
            take n;
        }
    }
}