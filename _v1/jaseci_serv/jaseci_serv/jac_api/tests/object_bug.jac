node state {
    has name;
    can process {}
}
node walk_root:state {
    has name = "walk_root";
    can process {
        visitor.next_state = --> node::a;
    }
}
node a:state {
    has name="A";
    can process {
        visitor.response = "I am at A";
        visitor.next_state = --> node::b;
    }
}
node b:state {
    has name="B";
    can process {
        visitor.response = "I am at B";
        visitor.next_state = --> node::c;
    }
}
node c:state {
    has name="C";
    can process {
        visitor.response = "I am at C";
        spawn visitor.prev_state walker::where_am_i;
        visitor.next_state = null;
    }
}

graph walk_graph {
    has anchor walk_root;
    spawn {
        walk_root = spawn node::walk_root;
        node_a = spawn walk_root ++> node::a;
        node_b = spawn node_a ++> node::b;
        node_c = spawn node_b ++> node::c;
    }
}

walker where_am_i {
    std.log("I am at " + here.name);
}
walker test_walk {
    has prev_state;
    has next_state;
    has response;
    root: take --> node::walk_root;

    state {
        here::process;
        if(response) {

            yield report {
                "response": response
            };
        }
        if(next_state) {
            prev_state = here;
            take next_state;
        }
    }

}
walker init {
    root {
        take --> node::graph_root else {
            spawn here ++> graph::walk_graph;
        }
    }
}