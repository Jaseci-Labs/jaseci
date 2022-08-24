import {*} with "./nodes.jac";
import {*} with "./edges.jac";
import {*} with "./main.jac";
import {*} with "./globals.jac";

walker empty {}

test "testing faq and va flows"
with graph::tesla_sales_rep by walker::empty {
    flows = file.load_json("data/tests.json");
    
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

test "testing a single query"
with graph::tesla_sales_rep by walker::talk(question="Hey I would like to go on a test drive"){
    res = std.get_report();
    assert(res[-1] == "To set you up with a test drive, we will need your name and address.");
}