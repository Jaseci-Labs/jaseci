node faq_root:cai_state {
    can use.qa_classify;
    can nlu {
        if (!visitor.wlk_ctx["prev_state"]) {
            answers = -->.answer;
            best_answer = use.qa_classify(
                text = visitor.question,
                classes = answers
            );
            visitor.wlk_ctx["intent"] = best_answer["match"];
        }
    }
    can process {
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        else {
            for n in --> {
                if (n.context["answer"] == visitor.wlk_ctx["intent"]){
                    visitor.wlk_ctx["next_state"] = n;
                    break;
                }
            }
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {
        visitor.response = "I can answer a variety of FAQs related to Tesla. What can I help you with?";
    }
}
node faq_state {
    has question;
    has answer;
    can nlg {
        visitor.response = here.answer;
    }
}

// Static graph definition
graph tesla_ai {
    has anchor dialogue_root;
    spawn {
        dialogue_root = spawn node::dialogue_root;
        test_drive_state = spawn node::test_drive_state;
        td_confirmation = spawn node::td_confirmation;
        td_confirmed = spawn node::td_confirmed;
        td_canceled = spawn node::td_canceled;

        dialogue_root +[intent_transition(intent="test drive")]+> test_drive_state;
        test_drive_state +[intent_transition(intent="cancel")]+> td_canceled;
        test_drive_state +[entity_transition(entities=["name", "address"])]+> td_confirmation;
        test_drive_state +[intent_transition(intent="provide name or address")]+> test_drive_state;
        td_confirmation +[intent_transition(intent="yes")]+> td_confirmed;
        td_confirmation +[intent_transition(intent="no")]+> test_drive_state;
        td_confirmation +[intent_transition(intent="cancel")]+> td_canceled;

        faq_root = spawn graph::faq;
        dialogue_root +[intent_transition(intent="i have a question")]+> faq_root;
    }
}

walker init {
    root {
        spawn here ++> graph::tesla_ai;
        spawn here walker::ingest_faq(kb_file="tesla_faq.json");
        spawn here walker::ask;
    }
}

// walker ask {
//     has question;
//     root {
//         question = std.input("AMA > ");
//         take --> node::faq_root;
//     }
//     faq_root {
//         take --> node::faq_state(question==question);
//     }
//     faq_state {:
//         std.out(here.answer);
//     }
// }

//use_qa model
walker ask {
    can use.qa_classify;
    has question;
    root {
        question = std.input(">");
        take --> node::faq_root;
    }
    faq_root {
        answers = -->.answer;
        best_answer = use.qa_classify(
            text = question,
            classes = answers
        );
        take --> node::faq_state(answer==best_answer["match"]);
    }
    faq_state {
        std.out(here.answer);
    }
}

walker ingest_faq {
    has kb_file;
    root: take --> node::faq_root;
    faq_root {
        kb = file.load_json(kb_file);
        for faq in kb {
            answer = faq["answer"];
            spawn here ++> node::faq_state(answer=answer);
        }
    }
}