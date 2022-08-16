import {*} with "./nodes.jac";
import {*} with "./edges.jac";

walker talk {
    has question="", interactive=false;
    has if_nlu=false;
    has question_type;
    has predicted_intent = null, extracted_entities = {}, matched_answer = null;
    has response;

    root {
        take --> node::cai_root;
    }

    cai_root {
        if (question == "" and interactive) {
            question = std.input("> ");
        }
        here::categorize;
        if (question_type == "va"):
            take --> node::va_state;
        elif (question_type == "faq"):
            take --> node::faq_state;
    }

    cai_state {
        if (question == "" and interactive) {
            question = std.input("> ");
        }

        if (!if_nlu) {
            predicted_intent = null;
            here::nlu;
            if_nlu = true;
        } else {
            # Clear the predicted intent if a NLU based transition has happened
            # This is to prevent infinite loop in certain situation
            predicted_intent = null;
        }

        take -[entity_transition(entities==extracted_entities.d::keys)]-> node::cai_state else {
            take -[intent_transition(intent==predicted_intent)]-> node::cai_state else {
                take -[answer_transition(answer==matched_answer)]-> node::cai_state else {
                    here::nlg;
                    question = "";
                    if_nlu = false;
                    if ((-->).length == 0):
                        take net.root();
                    else:
                        take here;
                    if (interactive): std.out(response);
                    else: yield report response;
                }
            }
        }
    }
}

walker ingest_faq {
    has kb_file;
    root: take --> node::faq_state;
    faq_state {
        kb = file.load_json(kb_file);
        for faq in kb {
            answer = faq["answer"];
            spawn here -[answer_transition(answer=answer)]-> node::faq_state(answer=answer);
        }
    }
}

graph tesla_sales_rep {
    has anchor cai_root;
    spawn {
        # Top level root
        cai_root = spawn node::cai_root;

        # Action-oriented VA
        state_cai_va_root = spawn node::cai_va_root;
        state_collect_info  = spawn node::collect_info;
        state_confirmation = spawn node::confirmation;
        state_confirmed = spawn node::confirmed;
        state_canceled = spawn node::canceled;

        state_cai_va_root -[intent_transition(
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

        # FAQ
        faq_root = spawn node::faq_state;

        # Connect to root
        cai_root --> state_cai_va_root;
        cai_root --> faq_root;
    }
}

walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
        take -->;
    }
    cai_root {
        take --> node::faq_state;
    }
    faq_state {
        spawn here walker::ingest_faq(kb_file="tesla_faq.json");
    }
}

walker interactive {
    root {
        spawn here walker::init;
        spawn here walker::talk;
    }
}

walker init_faq {
    root {
        spawn here --> node::faq_state;
        take --> node::faq_state;
    }
    faq_state {
        spawn here walker::ingest_faq(kb_file="tesla_faq.json");
    }
}

walker interactive_faq {
    root {
        spawn here walker::init_faq;
        spawn here walker::talk;
    }
}
