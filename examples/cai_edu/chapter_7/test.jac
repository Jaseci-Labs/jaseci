import {*} with "./nodes.jac";
import {*} with "./edges.jac";
import {*} with "./main.jac";
import {*} with "./globals.jac";

graph empty {
    has anchor root;
    spawn {
        root = spawn node::cai_root;
    }
}

test "testing faq and va flows"
with graph::empty by walker::init {
    flows = file.load_json("data/tests.json");
    // cai_root = *(global.cai_root);
    
    for flow in flows {

        for step in flow["flow"] {

            spawn here walker::talk(
                question=step["query"]
            );

            res = std.get_report();

            assert(res[-1] == step["response"]);
        }
    }
}