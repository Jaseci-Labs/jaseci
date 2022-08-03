import {*} with "./nodes.jac";
import {*} with "./edges.jac";
import {*} with "./fixture.jac";
import {*} with "./cai.jac";
import {*} with "./globals.jac";

graph empty {
    has anchor root;
    spawn {
        root = spawn node::cai_root;
    }
}

test "test flows in master_tests.json"
with graph::empty by walker::init {
    std.log("in master test");
    flows = file.load_json("./cai_tests.json");
    cai_root = *(global.cai_root);
    for flow in flows {
        # Reset user
        spawn cai_root walker::update_user;
        std.log("\n====Testing flow: " + flow["test_name"] + "====");
        new_dialogue = true;
        for step in flow["flow"] {
            std.log("\tquery: " + step["query"]);
            spawn cai_root walker::talker(
                question=step["query"],
                start_new_dialogue=new_dialogue
            );
            new_dialogue = false;
            res = std.get_report();
            std.log(res[-1]["response"]);
            assert (res[-1]["name"] == step["state"]);
        }
    }
}
 
test "test FAQ URL injection"
with graph::empty by walker::init {
    cai_root = *(std.get_global("cai_root"));
    spawn cai_root walker::read(
        source_url="https://projects.fivethirtyeight.com/redlining/"
    );
    # check there are 10 answers state
    spawn cai_root walker::get_answer_states;
    res = std.get_report();
    assert(res.length == 11);
}

test "test FAQ URL cleanup"
with graph::empty by walker::init {
    cai_root = *(std.get_global("cai_root"));
    spawn cai_root walker::read(
        source_url="https://projects.fivethirtyeight.com/redlining/"
    );
    spawn cai_root walker::forget;
    spawn cai_root walker::get_answer_states;
    res = std.get_report();
    assert(res.length == 1);
}

test "test FAQ URL injection and answer"
with graph::empty by walker::init {
    cai_root = *(std.get_global("cai_root"));
    spawn cai_root walker::read(
        source_url="https://www.experian.com/blogs/ask-experian/how-higher-credit-score-can-help-you-save-on-mortgage/"
    );
    spawn cai_root walker::read(
        source_url="https://urban.org/policy-centers/housing-finance-policy-center/projects/reducing-racial-homeownership-gap"
    );
    spawn cai_root walker::read(
        source_url="https://projects.fivethirtyeight.com/redlining/"
    );
    spawn cai_root walker::read(
        source_url="https://www.quickenloans.com/learn/questions-to-ask-your-lender"
    );
    faqs = [
        "i want to learn more about credit score",
        "how do i check my credit score?",
        "is there any racial gap in homeownership?",
        "how do i find the best mortgage lender for me?",
        "how is my credit score calculated?"
    ];
    for question in faqs {

        spawn cai_root walker::talker(
            question=question
        );
        res = std.get_report();
        std.log(question);
        std.log(res[-1]);
        assert(res[-1]["name"] == "faq_answer");
    }
}