import {
    node::{state, cai_root}
} with "./nodes.jac";

import {*} with "./user.jac";

import {
    edge::{transition, user_link, conv_graph, faq_answer}
} with "./edges.jac";

import {
    node::{biencoder}
} with "./biencoder.jac";

import {
    node::{flair_ner}
} with "./flair_ner.jac";

import {*} with "./globals.jac";

# Definition of conversation state graph
graph conv_graph {
    has anchor conv_root;
    spawn {
        conv_root = spawn node::state(name="conv_root_state");
        faq_state = spawn node::faq_state;
        conv_root --> faq_state;

        global.conv_root_state = conv_root.info["jid"];
        global.faq_state = faq_state.info["jid"];

        default_faq_answer_state = spawn node::faq_answer_state(answer="Sorry I can't handle that just yet.");
        faq_state -[faq_answer]-> default_faq_answer_state;

        state_soc = spawn node::state(name="soc");
        state_eoc = spawn node::state(name="eoc");

        state_order = spawn node::state(name="order");
        state_order_confirmation = spawn node::state(name="order_confirmation");
        state_order_denial = spawn node::state(name="order_denial");

        global_states = [
            [state_soc, global.soc_label],
            [state_eoc, global.eoc_label],
            [state_order, global.order_label]
        ];


        conv_root -[transition(intent_label = global.soc_label)]-> state_soc;
        conv_root -[transition(intent_label = global.eoc_label)]-> state_eoc;
        conv_root -[transition(intent_label = global.order_label)]-> state_order;

        state_order -[transition(intent_label = global.yes_label)]-> state_order_confirmation;
        state_order -[transition(intent_label = global.no_label)]-> state_order_denial;

        for gstate in global_states {
            state_order -[transition(intent_label = gstate[1])]-> gstate[0];
        }

    }
}

walker init {
    has prod = true, load_model = false, load_actions = true;

    # Name of models to load and use for this CAI
    has models_to_load = {
        "biencoder": "clf_model",
        "flair_ner": "ner_model"
    };

    root {
        here !--> -->;
        spawn here --> node::cai_root;
        take --> node::cai_root;
    }
    cai_root {
        global.cai_root = here.info["jid"];

        if(load_actions){
            if(prod){
                std.actload_remote("https://use-enc.jaseci.org/");
                std.actload_remote("https://use-qa.jaseci.org/");
                std.actload_remote("https://summarization.jaseci.org");
                std.actload_remote("https://tfm-ner.jaseci.org");
                std.actload_remote("https://flair-ner.jaseci.org");
                std.actload_remote("https://bi-enc-internal.jaseci.org");

            }else {
                std.actload_local("../../jaseci_kit/jaseci_kit/use_enc/use_enc.py");
                std.actload_local("../../jaseci_kit/jaseci_kit/entity_extraction/entity_extraction.py");
                std.actload_local("../../jaseci_kit/jaseci_kit/use_qa/use_qa.py");
                // std.actload_local("jskit-hlp/poa/hlp_poa.py");
            }
        }

        spawn here -[conv_graph]-> graph::conv_graph;
        spawn here --> node::user_dir;

        spawn here --> node::biencoder;
        spawn here --> node::flair_ner;
        spawn here --> node::use_encoder;

        take --> node::biencoder;
        take --> node::flair_ner;
        take --> node::use_encoder;
 
        take --> node::state;
        take --> node::user_dir;
   }

    state {
        if (here.name == "conv_root_state") {
            take --> node::faq_state;
        }
    }
    user_dir {
        take -[user_link]-> node::user;
    }
}