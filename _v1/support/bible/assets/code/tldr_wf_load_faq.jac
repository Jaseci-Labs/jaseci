import {edge::{trans_ner, trans_intent, trans_qa}} with "./edges.jac";
import {node::{state, hop_state}} with "./nodes.jac";

graph faq_gph {
    has anchor faq_root;
    spawn {
        faq_root = spawn node::state(name="Faq Root");

        answers = file.load_str('./faq_answers.txt').str::split('&&&');

        for i in answers:
            spawn faq_root -[trans_qa]-> node::state(response=i);
    }

}