import {*} with "./nodes.jac";
import {*} with "./edges.jac";

walker talk {
    has question="", interactive=true;
    has if_nlu=false;
    has predicted_intent, extracted_entities;
    has response;

    root {
        take --> node::cai_state;
    }

    # cai_state {
    cai_root, collect_info, confirmation, confirmed, canceled {
        std.out("at cai_state");
        if (interactive and question == "") {
            question = std.input("> ");
            if_nlu = false;
        }

        if (!if_nlu) {
            predicted_intent = null;
            extracted_entities = null;
            here::nlu;
            if_nlu = true;
        }

        take -[entity_transition(entities==extracted_entities.d::keys)]-> node::cai_state else {
            take -[intent_transition(intent==predicted_intent)]-> node::cai_state else {
                here::nlg;
                if (interactive) {
                    std.out(response);
                    question = "";
                    take here;
                } else: report repsonse;
            }
        }
    }
}

graph tesla_sales_rep {
    has anchor state_cai_root;
    spawn {
        state_cai_root = spawn node::cai_root;
        state_collect_info  = spawn node::collect_info;
        state_confirmation = spawn node::confirmation;
        state_confirmed = spawn node::confirmed;
        state_canceled = spawn node::canceled;

        state_cai_root -[intent_transition(
            intent = "test drive"
        )]-> state_collect_info;

        state_collect_info -[entity_transition(
            entities = ["name", "address"]
        )]-> state_confirmation;

        state_confirmation -[intent_transition(
            intent = "yes"
        )]-> state_confirmed;

        state_confirmation -[intent_transition(
            intent = "no"
        )]-> state_collect_info;

        state_collect_info -[intent_transition(
            intent = "cancel"
        )]-> state_canceled;

        state_confirmation -[intent_transition(
            intent = "cancel"
        )]-> state_canceled;
    }
}

walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
    }
}