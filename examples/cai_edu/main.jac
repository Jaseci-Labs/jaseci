import {*} with "./nodes.jac";
import {*} with "./edges.jac";

walker talk {
    has question;
    has predicted_intent, extracted_entities;
    has traveled = false;
    has response;

    cai_state {
        if (!traveled) {
            ::nlu;
            take -[entity_transition(entities=extract_entities.d:keys)]-> else {
                take -[intent_transition(intent=predicted_intent)] -> else {
                    take here;
                }
            }
            traveled = true;
        } else {
            ::nlg;
            report {"response": response};
        }
    }
}

graph tesla_sales_rep {
    has anchor state_cai_root;
    spawn {
        state_cai_root = spanw node::cai_root;
        state_collect_info  = spawn node::collect_info;
        state_confirmation = spawn node::confirmation;
        state_confirmed = spawn node::confirmed;
        state_canceled = spawn node::canceled;

        state_cai_root -[intent_transition(
            intent = "I would like to test drive"
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

walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
    }
}