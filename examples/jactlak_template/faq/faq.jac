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
        visitor.response = "What can I help you with?";
    }
}

node faq_state:cai_state {
    has question;
    has answer;
    can nlg {
        visitor.response = here.answer;
    }
}

// Static graph definition
graph faq {
    has anchor faq_root;
    spawn {

        // Spawning the nodes
        faq_root = spawn node::faq_root;
        faq_answer_1 = spawn node::faq_state(
            question="what's your name",
            answer="Hey, I'm JacTalk."
        );
        faq_answer_2 = spawn node::faq_state(
            question="what's should i call you",
            answer="You can call me JacTalk."
        );
        faq_answer_3 = spawn node::faq_state(
            question="are you a bot",
            answer="Yeah, I have been built by human."
        );

        // Connecting the nodes together
        faq_root ++> faq_answer_1;
        faq_root ++> faq_answer_2;
        faq_root ++> faq_answer_3;
    }
}

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

walker init {
    root {
        spawn here ++> node::faq_root;
        spawn here walker::ingest_faq(kb_file="faq.json");
        spawn here walker::ask;
    }
}