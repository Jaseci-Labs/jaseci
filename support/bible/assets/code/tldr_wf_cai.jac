import {node::{state, hop_state}} with "./nodes.jac";
import {edge::{trans_ner, trans_intent, trans_qa}} with "./edges.jac";
import {graph::basic_gph} with "./static_conv.jac";
import {graph::faq_gph} with "./load_faq.jac";



walker init {
    root {
        spawn here --> graph::basic_gph;
        spawn -->[0] -[trans_intent(intent="about chat bots")]-> graph::faq_gph;
    }
    with exit {
        spawn -->[0] walker::talker;
    }
}

walker talker {
    has utterance="";
    has use_cmd = true, path = [];
    if(use_cmd and here.details['name'] != 'hop_state'):
        utterance = std.input("> ");
    take -->;
}
