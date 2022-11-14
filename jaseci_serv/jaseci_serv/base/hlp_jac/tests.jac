import {*} with "./nodes.jac";
import {*} with "./edges.jac";
import {*} with "./fixture.jac";
import {*} with "./cai.jac";
import {*} with "./globals.jac";
import {*} with "./pdf_sum.jac";

graph empty {
    has anchor root;
    spawn {
        root = spawn node::cai_root;
    }
}

test "test flows in master_tests.json"
with graph::empty by walker::init {
    std.log("in master test");
    flows = file.load_json("/json_data/master_tests.json");
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
            # assert (step["response_contains"] in res[-1]["response"]);
        }
    }
}

// test "testing the three new states that was created"
// with graph::empty by walker::init {
//         cai_root = *(global.cai_root);

//         spawn cai_root walker::update_user;

//         labels = ["improve chances of loan approval", "page size improvement", "plan page improvement", "kind of loan"];

//         for label in labels:
//             spawn cai_root walker::talker(
//                 overwrite_intent=label,
//                 overwrite_entity=[]
//             );


//             res = std.get_report();
//             assert(res[-1]["response"]["success"] == true);
// }

// test "testing hlps api"
// with graph::empty by walker::init {
//         cai_root = *(global.cai_root);

//         id=1;

//         borrower_api = spawn cai_root walker::api(user_id=id, endpoint="kevBorrower");
//         financial_api = spawn cai_root walker::api(user_id=id, endpoint="borrowerFinancial");
//         credit_api = spawn cai_root walker::api(user_id=id, endpoint="borrowerCredit");


//         res = std.get_report();
//         assert(res[0]['success'] == true);
//         assert(res[1]['success'] == true);
//         assert(res[2]['success'] == true);

// }

// test "testing if hlp api payload is being process through the user query"
// with graph::empty by walker::init {
//         cai_root = *(global.cai_root);

//         spawn cai_root walker::update_user;

//         # this test will tell us if it grabs credit score dynamically from the hlp's api
//         spawn cai_root walker::talker(
//             question="How could I increase my chances for getting my loan approved?"
//         );

//         res = std.get_report();
//         std.log(res);
//         assert(res.length > 0);
// }


// test "testing pdf scraper with urls and pdfs"
// with graph::empty by walker::init {
//     cai_root = *(global.cai_root);

//     online_pdfs = file.load_json("./pdf_test.json");

//     # returns all url data
//     for pdf in online_pdfs:
//         spawn cai_root walker::pdf_summarization(pdf=pdf['url'], path=null, sentence_count=10);

//         // spawn cai_root walker::pdf_summarization(pdf=null, path=pdf['path'], sentence_count=1);

//         res = std.get_report();
//         std.log(res);
//         assert(res.length > 0);
// }

// test "test user data for extracting profile data"
// with graph::empty by walker::init {
//     cai_root = *(global.cai_root);
//     spawn cai_root walker::update_user;
// }

# walker get_answer_states {
#     cai_root: take --> node::state(name=="conv_root_state");
#     state: take --> node::faq_state;
#     faq_state: take -[faq_answer]-> node::faq_answer_state;
#     faq_answer_state: report here.answer;
# }
#
# test "test FAQ URL injection"
# with graph::empty by walker::init {
#     cai_root = *(std.get_global("cai_root"));
#     spawn cai_root walker::read(
#         source_url="https://projects.fivethirtyeight.com/redlining/"
#     );
#     # check there are 10 answers state
#     spawn cai_root walker::get_answer_states;
#     res = std.get_report();
#     assert(res.length == 11);
# }
#
# test "test FAQ URL cleanup"
# with graph::empty by walker::init {
#     cai_root = *(std.get_global("cai_root"));
#     spawn cai_root walker::read(
#         source_url="https://projects.fivethirtyeight.com/redlining/"
#     );
#     spawn cai_root walker::forget;
#     spawn cai_root walker::get_answer_states;
#     res = std.get_report();
#     assert(res.length == 1);
# }
#
# test "test FAQ URL injection and answer"
# with graph::empty by walker::init {
#     cai_root = *(std.get_global("cai_root"));
#     spawn cai_root walker::read(
#         source_url="https://www.experian.com/blogs/ask-experian/how-higher-credit-score-can-help-you-save-on-mortgage/"
#     );
#     spawn cai_root walker::read(
#         source_url="https://urban.org/policy-centers/housing-finance-policy-center/projects/reducing-racial-homeownership-gap"
#     );
#     spawn cai_root walker::read(
#         source_url="https://projects.fivethirtyeight.com/redlining/"
#     );
#     spawn cai_root walker::read(
#         source_url="https://www.quickenloans.com/learn/questions-to-ask-your-lender"
#     );
#     faqs = [
#         "i want to learn more about credit score",
#         "how do i check my credit score?",
#         "is there any racial gap in homeownership?",
#         "how do i find the best mortgage lender for me?",
#         "how is my credit score calculated?"
#     ];
#     for question in faqs {
#
#         spawn cai_root walker::talker(
#             question=question
#         );
#         res = std.get_report();
#         std.log(question);
#         std.log(res[-1]);
#         assert(res[-1]["name"] == "faq_answer");
#     }
# }