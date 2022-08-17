import {*} with "./nodes.jac";
import {*} with "./edges.jac";

walker talk {
    has question;
    has intent_override, entity_override;
    has predicted_intent, extracted_entities;
    has traveled = false;
    has response;

    cai_state {
        if (!traveled) {
            here::nlu;
            # Entity transition takes precedance over intent transition
            take -[entity_transition(entities=extracted_entities.d::keys)]-> node::cai_state else {
                take -[intent_transition(intent=predicted_intent)]-> node::cai_state else {
                    # Fall back to stay at current state if no valid transitions can be taken
                    take here;
                }
            }
            traveled = true;
        } else {
            here::nlg;
            report response;
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
}

walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
    }
}